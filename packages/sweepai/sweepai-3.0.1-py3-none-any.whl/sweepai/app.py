from __future__ import annotations

import asyncio
import ctypes
import os
import threading
import time
from contextlib import asynccontextmanager
from typing import Optional

import sentry_sdk
from fastapi import Body, Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from github import GithubException
from loguru import logger
from sentry_sdk import set_user

from sweepai.backend.api import app as backend_app
from sweepai.backend.api import fix_issue
from sweepai.backend.api_utils import get_token_header, message_cache
from sweepai.background_jobs import delete_old_repos, scheduler
from sweepai.config.client import SweepConfig
from sweepai.config.server import (
    BLACKLISTED_USERS,
    DISABLED_REPOS,
    ENV,
    GITHUB_LABEL_COLOR,
    GITHUB_LABEL_DESCRIPTION,
    GITHUB_LABEL_NAME,
    PREWARM_REPOS,
    SENTRY_URL,
)
from sweepai.core.entities import Message, PRChangeRequest, Snippet
from sweepai.core.github_utils import get_github_client
from sweepai.handlers.on_comment import on_comment
from sweepai.handlers.on_jira_ticket import handle_jira_ticket
from sweepai.handlers.on_push import on_push
from sweepai.handlers.on_revert_commit_comment import on_revert_commit_comment
from sweepai.handlers.on_ticket import on_ticket
from sweepai.o11y.log_utils import suppress_with_warning
from sweepai.review.auto_suggestions import provide_auto_suggestions
from sweepai.review.review_pr import review_pr
from sweepai.utils.str_utils import BOT_SUFFIX, get_hash
from sweepai.utils.ticket_rendering_utils import PR_REVERT_BUTTON, PR_REVERTED_INDICATOR
from sweepai.web.events import (
    CheckRunCompleted,
    CommentCreatedOrEditedRequest,
    IssueCommentRequest,
    IssueRequest,
    PRLabeledRequest,
    PRRequest,
)
from sweepai.web.global_threads import global_threads
from sweepai.web.health import health_check
from sweepai.web.safe_pqueue import SafePriorityQueue
from sweepai.web.startup import prewarm_search_index
from sweepai.web.sync_clock import sync_time
from sweepai.web.validate_license import validate_license
from sweepai.web.webhook_secret import verify_signature

version = time.strftime("%y.%m.%d.%H")

events = {}
on_ticket_events = {}
review_pr_events = {}
on_push_events = {}

security = HTTPBearer()

templates = Jinja2Templates(directory="sweepai/web")
logger.bind(application="webhook")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if SENTRY_URL:
        sentry_sdk.init(
            dsn=SENTRY_URL,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            release=version,
        )
    os.makedirs(message_cache, exist_ok=True)
    scheduler.start()
    yield
    with suppress_with_warning(KeyboardInterrupt):
        delete_old_repos()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(backend_app.router, prefix="/backend")


@app.middleware("http")
async def redirect_chat_backend_routes(request: Request, call_next):
    # For backwards compatibility, redirect /chat/backend/ to /backend/
    if request.url.path.startswith("/chat/backend/"):
        request.scope["path"] = request.url.path.replace("/chat/backend/", "/backend/", 1)
        request.scope["raw_path"] = request.scope["path"].encode()

    response = await call_next(request)
    return response


def run_on_ticket(*args, **kwargs):
    tracking_id = get_hash()
    return asyncio.run(on_ticket(*args, **kwargs, tracking_id=tracking_id))


def run_on_comment(*args, **kwargs):
    tracking_id = get_hash()
    with logger.contextualize(
        **kwargs,
        name="comment_" + kwargs["username"],
        tracking_id=tracking_id,
    ):
        asyncio.run(on_comment(*args, **kwargs, tracking_id=tracking_id))


def run_review_pr(*args, **kwargs):
    tracking_id = get_hash()
    with logger.contextualize(
        **kwargs,
        name="review_" + kwargs["username"],
        tracking_id=tracking_id,
    ):
        review_pr(*args, **kwargs, tracking_id=tracking_id)


def run_on_push(*args, **kwargs):
    tracking_id = get_hash()
    with logger.contextualize(
        **kwargs,
        name="push_" + kwargs["repo_full_name"],
        tracking_id=tracking_id,
    ):
        on_push(*args, **kwargs, tracking_id=tracking_id)


def terminate_thread(thread):
    """Terminate a python threading.Thread."""
    try:
        if not thread.is_alive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("Invalid thread ID")
        elif res != 1:
            # Call with exception set to 0 is needed to cleanup properly.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as e:
        logger.exception(f"Failed to terminate thread: {e}")


def call_on_ticket(*args, **kwargs):
    global on_ticket_events
    key = f"{kwargs['repo_full_name']}-{kwargs['issue_number']}"  # Full name, issue number as key

    # Use multithreading
    # Check if a previous process exists for the same key, cancel it
    e = on_ticket_events.get(key, None)
    if e:
        logger.info(f"Found previous thread for key {key} and cancelling it")
        terminate_thread(e)

    thread = threading.Thread(target=run_on_ticket, args=args, kwargs=kwargs)
    on_ticket_events[key] = thread
    thread.start()
    global_threads.append(thread)


def call_on_comment(*args, **kwargs):  # TODO: if its a GHA delete all previous GHA and append to the end
    def worker():
        while not events[key].empty():
            task_args, task_kwargs = events[key].get()
            run_on_comment(*task_args, **task_kwargs)

    global events
    repo_full_name = kwargs["repo_full_name"]
    pr_id = kwargs["pr_number"]
    key = f"{repo_full_name}-{pr_id}"  # Full name, comment number as key

    if key not in events:
        events[key] = SafePriorityQueue()

    events[key].put(0, (args, kwargs))

    # If a thread isn't running, start one
    if not any(thread.name == key and thread.is_alive() for thread in threading.enumerate()):
        thread = threading.Thread(target=worker, name=key)
        thread.start()
        global_threads.append(thread)


# add a review by sweep on the pr
def call_review_pr(*args, **kwargs):
    global review_pr_events
    key = f"{kwargs['repository'].full_name}-{kwargs['pr'].number}"  # Full name, issue number as key

    # Use multithreading
    # Check if a previous process exists for the same key, cancel it
    e = review_pr_events.get(key, None)
    if e:
        logger.info(f"Found previous thread for key {key} and cancelling it")
        terminate_thread(e)

    thread = threading.Thread(target=run_review_pr, args=args, kwargs=kwargs)
    review_pr_events[key] = thread
    thread.start()
    global_threads.append(thread)


def call_on_push(*args, **kwargs):
    global on_push_events
    key = kwargs["repo_full_name"]  # Full name as key

    # Use multithreading
    # Check if a previous process exists for the same key, cancel it
    e = on_push_events.get(key, None)
    if e:
        logger.info(f"Found previous thread for key {key} and cancelling it")
        terminate_thread(e)

    thread = threading.Thread(target=run_on_push, args=args, kwargs=kwargs)
    on_push_events[key] = thread
    thread.start()
    global_threads.append(thread)


def call_on_revert_commit_comment(*args, **kwargs):
    tracking_id = get_hash()
    args = (*args, tracking_id)
    thread = threading.Thread(target=on_revert_commit_comment, args=args, kwargs=kwargs)
    thread.start()
    global_threads.append(thread)


@app.get("/health")
def redirect_to_health():
    return health_check()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    try:
        validate_license()
        license_expired = False
    except Exception as e:
        logger.warning(e)
        license_expired = True
    return templates.TemplateResponse(
        name="index.html",
        context={
            "version": version,
            "request": request,
            "license_expired": license_expired,
        },
    )


def handle_request(request_dict, event=None):
    """So it can be exported to the listen endpoint."""
    with logger.contextualize(tracking_id="main", env=ENV):
        action = request_dict.get("action")
        try:
            handle_event(request_dict, event)
        except Exception as e:
            logger.exception(str(e))
        logger.info(f"Done handling {event}, {action}")
        return {"success": True}


# @app.post("/")
async def validate_signature(
    request: Request,
    x_hub_signature: Optional[str] = Header(None, alias="X-Hub-Signature-256"),
):
    payload_body = await request.body()
    if not verify_signature(payload_body=payload_body, signature_header=x_hub_signature):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


@app.post("/", dependencies=[Depends(validate_signature)])
def webhook(
    request_dict: dict = Body(...),
    x_github_event: Optional[str] = Header(None, alias="X-GitHub-Event"),
):
    """Handle a webhook request from GitHub"""
    with logger.contextualize(tracking_id="main", env=ENV):
        action = request_dict.get("action", None)
        logger.info(f"Received event: {x_github_event}, {action}")
        return handle_request(request_dict, event=x_github_event)


@app.post("/jira")
def jira_webhook(
    request_dict: dict = Body(...),
) -> None:
    def call_jira_ticket(*args, **kwargs):
        thread = threading.Thread(target=handle_jira_ticket, args=args, kwargs=kwargs)
        thread.start()

    call_jira_ticket(event=request_dict)


# Set up cronjob for this
@app.get("/update_sweep_prs_v2")
def update_sweep_prs_v2(repo_full_name: str, installation_id: int):
    # Get a Github client
    _, g = get_github_client(installation_id)

    # Get the repository
    repo = g.get_repo(repo_full_name)
    config = SweepConfig.get_config(repo)

    try:
        branch_ttl = int(config.get("branch_ttl", 7))
    except Exception:
        branch_ttl = 7
    branch_ttl = max(branch_ttl, 1)

    # Get all open pull requests created by Sweep
    pulls = repo.get_pulls(state="open", head="sweep", sort="updated", direction="desc")[:5]

    # For each pull request, attempt to merge the changes from the default branch into the pull request branch
    try:
        for pr in pulls:
            try:
                # make sure it's a sweep ticket
                feature_branch = pr.head.ref
                if not feature_branch.startswith("sweep/") and not feature_branch.startswith("sweep_"):
                    continue
                if "Resolve merge conflicts" in pr.title:
                    continue
                if (
                    pr.mergeable_state != "clean"
                    and (time.time() - pr.created_at.timestamp()) > 60 * 60 * 24
                    and pr.title.startswith("[Sweep Rules]")
                ):
                    pr.edit(state="closed")
                    continue

                repo.merge(
                    feature_branch,
                    pr.base.ref,
                    f"Merge main into {feature_branch}",
                )
            except Exception as e:
                logger.warning(f"Failed to merge changes from default branch into PR #{pr.number}: {e}")
    except Exception:
        logger.warning("Failed to update sweep PRs")


def should_handle_comment(request: CommentCreatedOrEditedRequest | IssueCommentRequest):
    comment = request.comment.body
    return (
        (
            comment.lower().startswith(
                "sweep:"
            )  # we will handle all comments (with or without label) that start with "sweep:" or "@sweep"
            or comment.lower().startswith("@sweep")
        )
        and request.comment.user.type == "User"  # ensure it's a user comment
        and request.comment.user.login not in BLACKLISTED_USERS  # ensure it's not a blacklisted user
        and BOT_SUFFIX not in comment  # we don't handle bot commnents
    )


def should_handle_revert_commit_comment(
    request: IssueCommentRequest | CommentCreatedOrEditedRequest,
):
    previous_body = request.changes.previous_body
    current_body = request.comment.body
    previous_body_has_revert_button = PR_REVERT_BUTTON in previous_body
    current_body_has_reverted_indicator = PR_REVERTED_INDICATOR in current_body
    return previous_body_has_revert_button and current_body_has_reverted_indicator


def handle_event(request_dict, event):
    action = request_dict.get("action")
    username = request_dict.get("sender", {}).get("login")
    if username:
        set_user({"username": username})

    if repo_full_name := request_dict.get("repository", {}).get("full_name"):
        if repo_full_name in DISABLED_REPOS:
            logger.warning(f"Repo {repo_full_name} is disabled")
            return {"success": False, "error_message": "Repo is disabled"}

    match event, action:
        case "pull_request", "opened":
            try:
                pr_request = PRRequest(**request_dict)
                _, g = get_github_client(request_dict["installation"]["id"])
                repo = g.get_repo(request_dict["repository"]["full_name"])
                pr = repo.get_pull(request_dict["pull_request"]["number"])
                # check if review_pr is restricted
                allowed_repos = os.environ.get("PR_REVIEW_REPOS", "")
                allowed_repos_set = set(allowed_repos.split(",")) if allowed_repos else set()
                allowed_usernames = os.environ.get("PR_REVIEW_USERNAMES", "")
                allowed_usernames_set = set(allowed_usernames.split(",")) if allowed_usernames else set()
                # only call review pr if user names are allowed
                # defaults to all users/repos if not set
                if (not allowed_repos or repo.name in allowed_repos_set) and (
                    not allowed_usernames or pr.user.login in allowed_usernames_set
                ):
                    # run pr review
                    call_review_pr(
                        username=pr.user.login,
                        pr=pr,
                        repository=repo,
                        installation_id=pr_request.installation.id,
                    )
                provide_auto_suggestions(pr, tracking_id=get_hash())
            except Exception as e:
                logger.exception(f"Failed to review PR: {e}")
                raise e
        case "pull_request", "labeled":
            try:
                pr_request = PRLabeledRequest(**request_dict)
                # run only if sweep label is added to the pull request
                if GITHUB_LABEL_NAME in [label.name.lower() for label in pr_request.pull_request.labels]:
                    _, g = get_github_client(request_dict["installation"]["id"])
                    repo = g.get_repo(request_dict["repository"]["full_name"])
                    pr = repo.get_pull(request_dict["pull_request"]["number"])

                    # run pr review - no need to check for allowed users/repos if they are adding sweep label
                    call_review_pr(
                        username=pr.user.login,
                        pr=pr,
                        repository=repo,
                        installation_id=pr_request.installation.id,
                    )
                else:
                    logger.info("sweep label not in pull request labels")

            except Exception as e:
                logger.exception(f"Failed to review PR: {e}")
                raise e
        case "issues", "opened":
            request = IssueRequest(**request_dict)
            issue_title_lower = request.issue.title.lower()
            if issue_title_lower.startswith("sweep") or "sweep:" in issue_title_lower or "@sweep" in issue_title_lower:
                _, g = get_github_client(request.installation.id)
                repo = g.get_repo(request.repository.full_name)

                labels = repo.get_labels()
                label_names = [label.name for label in labels]

                if GITHUB_LABEL_NAME not in label_names:
                    try:
                        repo.create_label(
                            name=GITHUB_LABEL_NAME,
                            color=GITHUB_LABEL_COLOR,
                            description=GITHUB_LABEL_DESCRIPTION,
                        )
                    except GithubException as e:
                        if e.status == 422 and any(
                            error.get("code") == "already_exists" for error in e.data.get("errors", [])
                        ):
                            logger.warning(f"Label '{GITHUB_LABEL_NAME}' already exists in the repository")
                        else:
                            raise e
                current_issue = repo.get_issue(number=request.issue.number)
                current_issue.add_to_labels(GITHUB_LABEL_NAME)
        case "issue_comment", "edited":
            request = IssueCommentRequest(**request_dict)
            sweep_labeled_issue = GITHUB_LABEL_NAME in [label.name.lower() for label in request.issue.labels]
            # handle revert comment
            if should_handle_revert_commit_comment(request):
                call_on_revert_commit_comment(request)
            if (
                request.issue is not None
                and sweep_labeled_issue
                and request.comment.user.type == "User"
                and request.comment.user.login not in BLACKLISTED_USERS
                and not request.comment.user.login.startswith("sweep")
                and not (request.issue.pull_request and request.issue.pull_request.url)
            ):
                logger.info("New issue comment edited")
                request.issue.body = request.issue.body or ""
                request.repository.description = request.repository.description or ""

                if not request.comment.body.strip().lower().startswith(GITHUB_LABEL_NAME):
                    logger.info("Comment does not start with 'Sweep', passing")
                    return {
                        "success": True,
                        "reason": "Comment does not start with 'Sweep', passing",
                    }

                call_on_ticket(
                    title=request.issue.title,
                    summary=request.issue.body,
                    issue_number=request.issue.number,
                    username=request.issue.user.login,
                    repo_full_name=request.repository.full_name,
                    installation_id=request.installation.id,
                    is_first_sweep_invocation=False,  # this is an edit
                )
            elif (
                request.issue.pull_request
                and request.comment.user.type == "User"
                and request.comment.user.login not in BLACKLISTED_USERS
            ):
                if should_handle_comment(request):
                    logger.info(f"Handling comment on PR: {request.issue.pull_request}")
                    pr_change_request = PRChangeRequest(
                        params={
                            "repo_full_name": request.repository.full_name,
                            "username": request.comment.user.login,
                            "installation_id": request.installation.id,
                            "pr_number": request.issue.number,
                            "comment_id": request.comment.id,
                        },
                    )
                    call_on_comment(**pr_change_request.params)
        case "issues", "edited":
            request = IssueRequest(**request_dict)
            if (
                GITHUB_LABEL_NAME in [label.name.lower() for label in request.issue.labels]
                and request.sender.type == "User"
                and not request.sender.login.startswith("sweep")
            ):
                logger.info("New issue edited")
                call_on_ticket(
                    title=request.issue.title,
                    summary=request.issue.body,
                    issue_number=request.issue.number,
                    username=request.issue.user.login,
                    repo_full_name=request.repository.full_name,
                    installation_id=request.installation.id,
                    is_first_sweep_invocation=False,  # this is an edit
                )
            else:
                logger.info("Issue edited, but not a sweep issue")
        case "issues", "labeled":
            request = IssueRequest(**request_dict)
            if (
                any(label.name.lower() == GITHUB_LABEL_NAME for label in request.issue.labels)
                and not request.issue.pull_request
            ):
                request.issue.body = request.issue.body or ""
                request.repository.description = request.repository.description or ""
                call_on_ticket(
                    title=request.issue.title,
                    summary=request.issue.body,
                    issue_number=request.issue.number,
                    username=request.issue.user.login,
                    repo_full_name=request.repository.full_name,
                    installation_id=request.installation.id,
                    is_first_sweep_invocation=True,  # issue labeled is the first invocation
                )
        case "issue_comment", "created":
            request = IssueCommentRequest(**request_dict)
            if (
                request.issue is not None
                and GITHUB_LABEL_NAME in [label.name.lower() for label in request.issue.labels]
                and request.comment.user.type == "User"
                and request.comment.user.login not in BLACKLISTED_USERS
                and not (request.issue.pull_request and request.issue.pull_request.url)
                and BOT_SUFFIX not in request.comment.body
            ):
                request.issue.body = request.issue.body or ""
                request.repository.description = request.repository.description or ""

                if not request.comment.body.strip().lower().startswith(GITHUB_LABEL_NAME):
                    logger.info("Comment does not start with 'Sweep', passing")
                    return {
                        "success": True,
                        "reason": "Comment does not start with 'Sweep', passing",
                    }

                call_on_ticket(
                    title=request.issue.title,
                    summary=request.issue.body,
                    issue_number=request.issue.number,
                    username=request.issue.user.login,
                    repo_full_name=request.repository.full_name,
                    installation_id=request.installation.id,
                    is_first_sweep_invocation=False,  # this is a new comment
                )
            elif (
                request.issue.pull_request
                and request.comment.user.type == "User"
                and request.comment.user.login not in BLACKLISTED_USERS
                and BOT_SUFFIX not in request.comment.body
            ):
                if should_handle_comment(request):
                    pr_change_request = PRChangeRequest(
                        params={
                            "repo_full_name": request.repository.full_name,
                            "username": request.comment.user.login,
                            "installation_id": request.installation.id,
                            "pr_number": request.issue.number,
                            "comment_id": request.comment.id,
                        },
                    )
                    call_on_comment(**pr_change_request.params)
        case "pull_request_review_comment", "created":
            request = CommentCreatedOrEditedRequest(**request_dict)
            if should_handle_comment(request):
                pr_change_request = PRChangeRequest(
                    params={
                        "repo_full_name": request.repository.full_name,
                        "username": request.comment.user.login,
                        "installation_id": request.installation.id,
                        "pr_number": request.pull_request.number,
                        "comment_id": request.comment.id,
                    },
                )
                call_on_comment(**pr_change_request.params)
        case "pull_request_review_comment", "edited":
            request = CommentCreatedOrEditedRequest(**request_dict)
            if should_handle_revert_commit_comment(request):
                call_on_revert_commit_comment(request)
            if should_handle_comment(request):
                pr_change_request = PRChangeRequest(
                    params={
                        "repo_full_name": request.repository.full_name,
                        "username": request.comment.user.login,
                        "installation_id": request.installation.id,
                        "pr_number": request.pull_request.number,
                        "comment_id": request.comment.id,
                    },
                )
                call_on_comment(**pr_change_request.params)
        case "check_run", "completed":
            request = CheckRunCompleted(**request_dict)
            pull_request_object = request.check_run.pull_requests[0]
            _, g = get_github_client(request.installation.id)
            repo = g.get_repo(request.repository.full_name)
            pull_request = repo.get_pull(pull_request_object.number)
            provide_auto_suggestions(pull_request, tracking_id=get_hash())
        case "installation_repositories", "added":
            # TODO: do a dummy query
            pass
        case "installation", "created":
            # TODO: do a dummy query
            pass
        case "push", None:
            call_on_push(repo_full_name=repo_full_name)
            # TODO: add this one later when we parse out push events correctly and actually fetch the PR
            # provide_auto_suggestions(pr, tracking_id=get_hash()) # might want to make this one async as well
        case "pull_request", "closed":
            pr_request = PRRequest(**request_dict)
            merged_by = pr_request.pull_request.merged_by.login if pr_request.pull_request.merged_by else None
            if merged_by is not None:
                # TODO: track merged prs here
                # TODO: do a dummy query
                pass
        case "ping", None:
            return {"message": "pong"}
        case _:
            return {"error": "Unsupported type"}


# make this a separate app later, but this is simpler for now


@app.post("/api/fix_issue")
async def fix_issue_endpoint(
    repo_name: str = Body(...),
    query: str = Body(...),
    messages: list[Message] = Body([]),
    snippets: list[Snippet] = Body([]),
    branch: str = Body(None),
    access_token: str = Depends(get_token_header),
):
    try:
        result = await fix_issue(
            repo_full_name=repo_name,
            query=query,
            messages=messages,
            snippets=snippets,
            access_token=access_token,
            branch=branch,
        )
        return result
    except Exception as e:
        logger.error(f"Error in unified_api_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    sync_time()
    for repo_identifier in PREWARM_REPOS:
        prewarm_search_index(repo_identifier)
