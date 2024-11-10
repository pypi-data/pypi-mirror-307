import json
import os
import secrets
import ssl
import subprocess
import time
import traceback
from typing import Iterator
import uuid
from copy import deepcopy
from datetime import datetime
from urllib.parse import urlencode

import httpx
from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from fastapi.responses import FileResponse, RedirectResponse
from github import Github, GithubException
from github.Repository import Repository
from loguru import logger

from sweepai.backend.api_utils import (
    check_repo_exists,
    get_authenticated_github_client,
    get_directory_summaries,
    get_github_client_from_org,
    get_pr_snippets,
    get_token_header,
    stream_state_diff,
    strip_branch_prefix,
)
from sweepai.backend.chat_agent import chat_agent, preprocess_messages  # 1s import
from sweepai.backend.pull_request_bot import (
    get_commit_message_for_diff,
    get_pr_summary_for_chat,
)
from sweepai.backend.request_rewriter import rewrite_query
from sweepai.config.server import (
    AUTHORIZED_USERNAMES,
    CACHE_DIRECTORY,
    CURL_CA_BUNDLE,
    FRONTEND_URL,
    GITHUB_API_BASE_URL,
    GITHUB_BASE_URL,
    GITHUB_ID,
    GITHUB_SECRET,
    WHITELISTED_USERS,
)
from sweepai.core.entities import (
    AssistantMessage,
    Message,
    Snippet,
    UserMessage,
    fuse_snippets,
)
from sweepai.core.github_utils import (
    ClonedRepo,
    CustomGithub,
    MockClonedRepo,
    clean_branch_name,
    commit_multi_file_changes,
    create_and_get_branch,
    get_github,
    get_installation_id,
    temporary_cloned_repo_copy,
    github_integration,
    get_token as get_token_from_installation,
)
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL
from sweepai.dataclasses.chat_agent_context import ChatAgentContext
from sweepai.dataclasses.check_status import (
    CheckStatus,
    gha_to_check_status,
    gha_to_message,
)
from sweepai.dataclasses.code_suggestions import CodeSuggestion
from sweepai.dataclasses.directory_summaries_request import DirectorySummariesRequest
from sweepai.dataclasses.file_modification_state import FileModificationState
from sweepai.dataclasses.fix_issue_result import FixIssueResult, PullRequestData
from sweepai.handlers.on_check_suite import get_failing_docker_logs
from sweepai.core.entities import organize_snippets
from sweepai.o11y.endpoint_wrapper import endpoint_wrapper
from sweepai.o11y.event_logger import posthog
from sweepai.o11y.log_utils import log_to_file, suppress_with_warning
from sweepai.o11y.posthog_trace import posthog_trace
from sweepai.search.agent.search_agent import file_searcher  # 1s import
from sweepai.search.query.ticket_utils import prep_snippets
from sweepai.utils.cache import create_cache
from sweepai.utils.commit_metrics import METRICS_FILE
from sweepai.utils.posthog_utils import (
    format_posthog_events_as_csv,
    read_posthog_events_from_disk,
)
from sweepai.utils.str_utils import (
    get_hash,
    object_to_xml,
    ordered_dedup,
    truncate_commit_message,
    wildcard_match,
)
from sweepai.utils.streamable_functions import cached_streamable, streamable
from sweepai.utils.ticket_rendering_utils import get_failing_gha_logs, hyperlink
from sweepai.utils.timer import Timer
from sweepai.web.heartbeat import StreamingResponseWithHeartbeat

app = FastAPI()
cache = create_cache()

### AUTH START ###


def generate_random_state(length=32):
    """Generate a secure random string for use as state parameter."""
    return secrets.token_urlsafe(length)


def get_redirect_uri_base(request: Request):
    origin = request.headers.get("Referer") or request.query_params.get("origin") or str(request.base_url)
    return origin.rstrip("/")


@app.get("/login")
async def login(request: Request):
    redirect_uri_base = get_redirect_uri_base(request)
    params = {
        "client_id": GITHUB_ID,
        "redirect_uri": f"{redirect_uri_base}/api/auth/callback/github",
        "scope": "repo user",
        "state": generate_random_state(),  # Function to generate a random state
    }

    auth_url = f"https://{GITHUB_BASE_URL}/login/oauth/authorize?{urlencode(params)}"

    return RedirectResponse(url=auth_url)


@app.get("/auth")
async def auth(request: Request):
    context = ssl.create_default_context(cafile=CURL_CA_BUNDLE) if CURL_CA_BUNDLE else True
    async_client = httpx.AsyncClient(verify=context, proxies={"all://": None} if CURL_CA_BUNDLE else None)
    async with async_client as client:
        code = request.query_params.get("code")
        state = request.query_params.get("state")

        assert state  # TODO: use the cache to verify the state against CSRF

        redirect_uri_base = get_redirect_uri_base(request)

        token_url = f"https://{GITHUB_BASE_URL}/login/oauth/access_token"
        data = {
            "client_id": GITHUB_ID,
            "client_secret": GITHUB_SECRET,
            "code": code,
            "redirect_uri": f"{redirect_uri_base}/api/auth/callback/github",
        }
        headers = {"Accept": "application/json"}

        response = await client.post(token_url, data=data, headers=headers)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")

            if access_token:
                github_user_url = f"{GITHUB_API_BASE_URL}/user"
                headers = {"Authorization": f"token {access_token}"}

                user_response = await client.get(github_user_url, headers=headers)

                if user_response.status_code == 200:
                    user_data = user_response.json()
                    username = user_data.get("login")
                    return {
                        "access_token": access_token,
                        "username": username,
                        "email": user_data.get("email"),
                        "name": user_data.get("name"),
                        "image": user_data.get("avatar_url"),
                    }
                else:
                    raise HTTPException(status_code=400, detail="Failed to obtain username")
            else:
                raise HTTPException(status_code=400, detail="Failed to obtain access token")
        else:
            raise HTTPException(status_code=response.status_code, detail="GitHub OAuth error")


### AUTH END ###


def get_github_client(repo_name: str = Body(...), access_token: str = Depends(get_token_header)) -> CustomGithub:
    with Timer() as timer:
        g = get_authenticated_github_client(repo_name, access_token)
    logger.debug(f"Getting authenticated GitHub client took {timer.time_elapsed} seconds")

    if not g:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The repository may not exist or you may not have access to this repository.",
        )

    return g


def get_org_github_client(repo_name: str = Body(...)) -> CustomGithub:
    org_name, repo_name_ = repo_name.split("/")
    _token, g = get_github_client_from_org(org_name)
    return g


def get_username(access_token: str = Depends(get_token_header)):
    try:
        login = Github(access_token, base_url=GITHUB_API_BASE_URL).get_user().login
        if not wildcard_match(login, WHITELISTED_USERS):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not whitelisted to use Sweep.",
            )
        return login
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"GitHub authentication failed: {str(e)}",
        ) from e


def is_admin(username: str = Depends(get_username)):
    if username not in AUTHORIZED_USERNAMES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this endpoint.",
        )


@app.post("/api/directory_summaries")
@endpoint_wrapper
def get_directory_summaries_endpoint(request: DirectorySummariesRequest, access_token: str = Depends(get_token_header)):
    """
    Retrieve directory summaries for the specified directories.

    This endpoint allows users to fetch summaries for up to 100 directories at a time.
    If a directory summary doesn't exist in the cache, an empty string is returned for that directory.

    Parameters:
    - request: DirectorySummariesRequest
        - repo_name: str (The full name of the repository, e.g., "owner/repo")
        - directories: List[str] (List of directory names to fetch summaries for)

    Returns:
    - dict: A dictionary mapping directory names to their summaries

    Raises:
    - HTTPException:
        - 400 if the number of requested directories exceeds 100
        - 401 if authentication fails
        - 403 if the user doesn't have access to the repository
    """
    if len(request.directories) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 100 directory summaries can be requested at once.",
        )

    try:
        get_github_client(request.repo_name, access_token)
    except HTTPException as e:
        raise e

    summaries = get_directory_summaries(request.repo_name, request.directories)
    return {"summaries": summaries}


@app.get("/api/metrics")
@endpoint_wrapper
def get_commit_metrics_endpoint(access_token: str = Depends(get_token_header), _: bool = Depends(is_admin)):
    return {}  # skipping because it doesn't work


@app.get("/api/metrics.csv")
@endpoint_wrapper
def get_commit_metrics_csv_endpoint(_: bool = Depends(is_admin)):
    logger.info(f"Getting commit metrics CSV from {METRICS_FILE}")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"metrics_{timestamp}.csv"

    response = FileResponse(METRICS_FILE, filename=filename)

    # Add cache-busting headers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


def get_token(
    g: CustomGithub = Depends(get_github_client),
    access_token: str = Depends(get_token_header),
):
    return g.token if isinstance(g, CustomGithub) else access_token


def get_repo(repo_name: str = Body(...), g: CustomGithub = Depends(get_github_client)):
    return g.get_repo(repo_name)


def get_cloned_repo(
    repo_name: str = Body(...),
    branch: str = Body(None),
    query: str = Body(""),
    annotations: dict = Body({}),
    access_token: str = Depends(get_token_header),
    repo: Repository = Depends(get_repo),
):
    return ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=branch)


@app.get("/repo")
@endpoint_wrapper
def check_repo_exists_endpoint(
    repo_name: str,
    access_token: str = Depends(get_token_header),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    _g = get_github_client(repo_name, access_token)
    username = Github(access_token, base_url=GITHUB_API_BASE_URL).get_user().login
    token = access_token
    result = check_repo_exists(
        username,
        repo_name,
        token,
        metadata={
            "repo_name": repo_name,
        },
    )
    try:
        CustomGithub.from_repo_full_name(repo_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Repository not found or not installed. Make sure to install the app on this repository.") from e

    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])

    background_tasks.add_task(
        check_repo_exists,
        username,
        repo_name,
        token,
        metadata={"repo_name": repo_name},
        do_clone=True,
    )

    return result

@app.post("/check_whitelist")
@endpoint_wrapper
def check_access(_username: str = Depends(get_username)):
    return Response(status_code=status.HTTP_200_OK, content="Successfully authenticated.")

# UNUSED: TODO: use this correctly
@app.get("/repos")
@endpoint_wrapper
def get_repos(access_token: str = Depends(get_token_header)):
    repos = []
    user_client = Github(access_token, base_url=GITHUB_API_BASE_URL)
    user = user_client.get_user()
    repos = list(user.get_repos(type="all", sort="pushed", direction="desc"))
    username = user.login

    try:
        installation = github_integration.get_user_installation(username)
    except GithubException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"GitHub authentication failed. Please install the app for your user.") from e
    else:
        token = get_token_from_installation(installation.id)
        # client = installation.get_github_for_installation()
        client = Github(token, base_url=GITHUB_API_BASE_URL)
        user = client.get_user(username)
        repos = list(user.get_repos(type="all", sort="pushed", direction="desc"))
        return [{"full_name": repo.full_name} for repo in repos]


@app.post("/branches")
@endpoint_wrapper
def get_branches(
    repo_name: str = Body(...),
    limit: int = Body(200),
    access_token: str = Depends(get_token_header),
    repo: Repository = Depends(get_repo),
    g: CustomGithub = Depends(get_github_client),
):
    repo_full_name = repo_name # TODO: change in frontend later
    # TODO: add integration tests
    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name)

    user = g.get_user()
    username = user.login
    first_name, *_ = user.name.split(" ") if user.name else (user.login, "")
    email = user.email
    command = f"git for-each-ref --format='%(committerdate) %09 %(authoremail) %09 %(authorname) %09 %(refname)' refs/remotes/origin | sort -k5n -k2M -k3n -k4n | grep -E '{first_name}|{username}|{email}'"
    # The next command ensures that the branch exists on remote but is too slow. Might add this in the future by adding filters.
    # command = f"""git ls-remote --heads origin | awk '{{print $2}}' | cut -d'/' -f3- | while read branch; do git for-each-ref --format='%(committerdate) %09 %(authoremail) %09 %(authorname) %09 %(refname)' refs/remotes/origin | sort -k5n -k2M -k3n -k4n | grep -E '{first_name}|{username}|{email}' | grep -E 'refs/remotes/origin/$branch'; done | sort -k1nr -k2M -k3nr -k4nr"""
    branches = subprocess.run(
        command, shell=True, text=True, capture_output=True, cwd=cloned_repo.repo_dir
    ).stdout.split("\n")
    branches = branches[::-1]
    branches = [line.split(" ")[-1] for line in branches if line]
    branches = [strip_branch_prefix(line) for line in branches]
    branches = ordered_dedup(branches)
    branches = [branch for branch in branches if branch not in ["HEAD", "main", "master"]]
    branches = branches[:limit]
    return branches


@app.post("/rewrite_query")
@endpoint_wrapper
def rewrite_query_endpoint(
    repo_name: str = Body(...),
    branch: str = Body(None),
    query: str = Body(...),
    pulls: list[dict] = Body([]),
    username: str = Depends(get_username),
    _github_client: CustomGithub = Depends(get_github_client),
):
    def stream() -> Iterator[tuple[str, str, list[dict]]]:
        yield "Cloning repository...", "", []
        cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=branch)
        yield "Repository cloned.", "", []
        for message, new_ticket, snippets in rewrite_query.stream(
            username,
            query,
            cloned_repo,
            pulls,
            context=ChatAgentContext(use_case="chat"),
        ):
            yield [
                message,
                (
                    f"# Original Request\n{query}\n\n{new_ticket}" if new_ticket else ""
                ),  # this renders the original request in the UI
                [snippet.model_dump() for snippet in snippets],
            ]

    return StreamingResponseWithHeartbeat(
        stream_state_diff(stream(), initial_state=("", [], "")),
        heartbeat_message=json.dumps([]),
    )


@app.post("/search")
@endpoint_wrapper
async def search_codebase_endpoint(
    repo_name: str = Body(...),
    query: str = Body(...),
    annotations: dict = Body({}),
    branch: str = Body(None),
    username: str = Depends(get_username),
    token: str = Depends(get_token),
):
    def stream_response():
        try:
            yield json.dumps(["Starting search...", []])
            for message, snippets in wrapped_search_codebase.stream(
                username,
                repo_name,
                query,
                token,
                annotations=annotations,
                branch=branch,
                metadata={
                    "repo_name": repo_name,
                    "query": query,
                },
                context=ChatAgentContext(use_case="chat"),
            ):
                yield json.dumps((message, [snippet.model_dump() for snippet in snippets]))
        except Exception as e:
            yield json.dumps({"status": "error", "error": f"{str(e)}"})

    return StreamingResponseWithHeartbeat(stream_response())


@streamable
def search_codebase(
    repo_name: str,
    query: str,
    access_token: str,
):
    with Timer() as timer:
        yield "Cloning repository...", []
        cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name)
        yield "Repository cloned.", []

        for message, snippets in prep_snippets.stream(cloned_repo, query, skip_analyze_agent=True):
            yield message, snippets
    snippets = fuse_snippets(snippets)
    yield "Fused snippets.", snippets
    logger.debug(f"Preparing snippets took {timer.time_elapsed} seconds")
    return snippets


@app.post("/search_agent")
@endpoint_wrapper
async def agentic_search_codebase_endpoint(
    repo_name: str = Body(...),
    branch: str = Body(None),
    query: str = Body(...),
    messages: list[Message] = Body([]),
    annotations: dict = Body({}),
    existing_snippets: list = Body([]),
    username: str = Depends(get_username),
    _github_client: CustomGithub = Depends(get_github_client),
):
    existing_snippets = [Snippet(**snippet) for snippet in existing_snippets]

    def stream_state() -> Iterator[tuple[str, list[Snippet], list[Message]]]:
        cleaned_repo_name = repo_name.replace("/", "--")
        with log_to_file(f"chat-search-agent-{username}-{cleaned_repo_name}-{get_hash()}"):
            yield "Cloning repository...", [], []
            cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=branch)
            yield "Starting search...", existing_snippets, []
            for message, snippets, messages_ in wrapped_file_searcher.stream(
                username=username,
                cloned_repo=cloned_repo,
                query=query,
                context=ChatAgentContext(use_case="chat"),
                messages=messages,
                existing_snippets=existing_snippets,
                annotations=annotations,
                metadata={
                    "repo_name": cloned_repo.repo_full_name,
                    "query": query,
                },
            ):
                yield message, snippets, messages_

    return StreamingResponseWithHeartbeat(
        stream_state_diff(
            [
                message,
                [snippet.model_dump() for snippet in snippets],
                [message_.model_dump() for message_ in messages_],
            ]
            for message, snippets, messages_ in stream_state()
        ),
        heartbeat_message=json.dumps([]),
    )


@cached_streamable(cache=cache, ignore_params=["access_token", "metadata"])
@posthog_trace
def wrapped_file_searcher(
    username: str,
    cloned_repo: ClonedRepo,
    query: str,
    context: ChatAgentContext,
    messages: list[Message] = [],
    existing_snippets: list[Snippet] = [],
    annotations: dict = {},
    metadata: dict = {},
    __version__: str = "v0.0",
):
    model = LATEST_CLAUDE_MODEL
    try:
        yield "Repository pulled.", existing_snippets, []
        if annotations:
            yield "Getting pull request snippets...", existing_snippets, []
            pr_snippets, _, pulls_messages = get_pr_snippets(
                cloned_repo.repo_full_name,
                annotations,
                cloned_repo,
                context=context,
            )
            existing_snippets = organize_snippets(existing_snippets + pr_snippets)
            existing_snippets = list(dict.fromkeys(existing_snippets))
            if pulls_messages.count("<pull_request>") > 1:
                query += "\n\nHere are the mentioned pull request(s):\n\n" + pulls_messages
            else:
                query += "\n\n" + pulls_messages
            yield "Got pull request snippets.", existing_snippets, []
        if len(messages) > 1:
            new_messages = []
            for message in messages:
                if message.role != "function":
                    new_messages.append(message)
                else:
                    # should probably pass tools here but this will do
                    # function input
                    content = message.function_call.get("thinking", "").strip("\n")
                    if message.function_call.get("function_name", "") != "deciding":
                        content += "\n\n" + object_to_xml(
                            message.function_call.get("function_parameters", {}),
                            message.function_call.get("function_name", ""),
                        )
                    message_key_suffix = f'_{message.key.split("_")[-1]}' if message.key else ""
                    new_messages.append(
                        Message(
                            content=content,
                            role="assistant",
                            key="function_call" + message_key_suffix,
                        )
                    )
                    if message.content:
                        # function output
                        new_messages.append(
                            Message(
                                content=message.content,
                                role="user",
                                key="function_call_output" + message_key_suffix,
                            )
                        )
            messages = new_messages
        for message, snippets, messages in file_searcher.stream(  # type: ignore
            username=username,
            question=query,
            cloned_repo=cloned_repo,
            messages=messages,
            existing_snippets=existing_snippets,
            model=model,
            use_case=context.use_case,
        ):
            yield message, snippets, messages
    except Exception as e:
        logger.exception(f"Error in wrapped_file_searcher: {str(e)}")
        posthog.capture(
            f"{username} wrapped_file_searcher",
            "wrapped_file_searcher error",
            properties={
                "error": str(e),
                "user": username,
                "repo": cloned_repo.repo_full_name,
                "query": query,
                "annotations": annotations,
                "branch": cloned_repo.branch,
                "metadata": metadata,
                "traceback": str(traceback.format_exc()),
            },
        )
        # add pdb postmortems here if needed
        raise e


@streamable
@posthog_trace
def wrapped_search_codebase(
    username: str,
    repo_name: str,
    query: str,
    access_token: str,
    context: ChatAgentContext,
    annotations: dict = {},
    branch: str = None,
    metadata: dict = {},
):
    yield "Cloning repository...", []
    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=branch)
    yield "Repository cloned.", []
    if annotations:
        yield "Processing pull request data...", []
        pr_snippets, skipped_pr_snippets, pulls_messages = get_pr_snippets(
            repo_name, annotations, cloned_repo, context=context
        )
        if pulls_messages.count("<pull_request>") > 1:
            query += "\n\nHere are the mentioned pull request(s):\n\n" + pulls_messages
        else:
            query += "\n\n" + pulls_messages
        yield "Got pull request snippets.", []
    for message, snippets in search_codebase.stream(
        repo_name,
        query,
        access_token,
    ):
        yield message, snippets


@app.post("/chat")
@endpoint_wrapper
def chat_codebase(
    repo_name: str = Body(...),
    messages: list[Message] = Body(...),
    snippets: list[Snippet] = Body(...),
    modify_files_dict: dict = Body({}),
    username: str = Depends(get_username),
    cloned_repo: MockClonedRepo = Depends(get_cloned_repo),
):
    if len(messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one message is required.",
        )

    last_user_message = next(
        (message.content for message in reversed(messages) if message.role == "user"),
        None,
    )
    if last_user_message is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user message found in the provided messages.",
        )

    # Parse code_entity_relationship_map and search agent solution
    code_entity_relationship_map, search_agent_solution, existing_patterns, messages = preprocess_messages(messages)

    diff_stream = stream_state_diff(
        [message.model_dump() for message in messages]
        for messages in chat_agent.stream(
            username,
            cloned_repo,
            messages,
            modify_files_dict,
            snippets,
            metadata={
                "repo_name": repo_name,
                "message": last_user_message,
                "messages": [message.model_dump() for message in messages],
                "snippets": [snippet.model_dump() for snippet in snippets],
                "code_entity_relationship_map": code_entity_relationship_map,
                "search_agent_solution": search_agent_solution,
                "existing_patterns": existing_patterns,
                "modify_files_dict": modify_files_dict,
            },
            context=ChatAgentContext(use_case="chat"),
        )
    )

    return StreamingResponseWithHeartbeat(
        diff_stream,
        heartbeat_message=json.dumps([]),
    )


@app.post("/commit_to_branch")
@endpoint_wrapper
async def commit_to_branch(
    repo_name: str = Body(...),
    file_changes: dict[str, str] = Body(...),
    branch: str = Body(""),
    base_branch: str = Body(""),
    commit_message: str = Body(""),
    access_token: str = Depends(get_token_header),
    g: CustomGithub = Depends(get_github_client),
    repo: Repository = Depends(get_repo),
):
    branch = branch or base_branch # for backwards compatibility, eventually remove this
    try:
        org_name, repo_name_ = repo_name.split("/")
        _token, g = get_github_client_from_org(org_name)  # TODO: handle users as well

        new_branch = create_branch_and_push_changes(
            repo=repo,
            repo_name=repo_name,
            access_token=access_token,
            branch=branch,
            file_changes=file_changes,
            base_branch=branch,
            title=commit_message,
            should_commit_to_branch=True,
        )

        return {
            "success": True,
            "new_branch": new_branch,
            "sha": new_branch,  # TODO (wzeng): I changed this and when we use the UI again we should access the actual sha
        }
    except GithubException as ge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub API error: {ge.data.get('message', str(ge))}",
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        logger.error(f"Unexpected error in commit_to_pull: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")


@app.post("/create_branch")
@endpoint_wrapper
def create_branch_endpoint(
    repo_name: str = Body(...),
    file_changes: dict[str, str] = Body(...),
    branch: str = Body(...),
    base_branch: str = Body(""),
    access_token: str = Depends(get_token_header),
    _g: CustomGithub = Depends(get_github_client),
    g: CustomGithub = Depends(get_org_github_client),
):
    try:
        _, repo_name_ = repo_name.split("/")

        repo = g.get_repo(repo_name)
        base_branch = base_branch or repo.default_branch

        new_branch = create_and_get_branch(repo, branch, base_branch).name

        cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=branch)
        with temporary_cloned_repo_copy(cloned_repo) as temp_repo:
            commit_multi_file_changes(
                temp_repo,
                file_changes,
                commit_message=f"Updated {len(file_changes)} files",
                branch=new_branch,
            )
        return {"success": True, "branch": new_branch}
    except GithubException as ge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub API error: {ge.data.get('message', str(ge))}",
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")


def create_branch_and_push_changes(
    repo: Repository,
    repo_name: str,
    access_token: str,
    branch: str,
    file_changes: dict[str, str],
    base_branch: str = "",
    title: str = "",
    should_commit_to_branch: bool = False,
):
    assert branch
    if should_commit_to_branch:
        new_branch_obj = repo.get_branch(branch)
    else:
        new_branch_obj = create_and_get_branch(repo=repo, branch=branch, base_branch=base_branch)
    new_branch = new_branch_obj.name

    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=new_branch)
    with temporary_cloned_repo_copy(cloned_repo) as temp_repo:
        if file_changes:
            commit_multi_file_changes(
                temp_repo,
                file_changes,
                commit_message=truncate_commit_message(title) or f"Updated {len(file_changes)} files",
                branch=new_branch,
            )
    return new_branch


@app.post("/create_pull")
@endpoint_wrapper
def create_pull(
    repo_name: str = Body(...),
    file_changes: dict[str, str] = Body(...),
    branch: str = Body(...),
    title: str = Body(...),
    body: str = Body(...),
    base_branch: str = Body(""),
    access_token: str = Depends(get_token_header),
    _g: CustomGithub = Depends(get_github_client),
    g: CustomGithub = Depends(get_org_github_client),
    username: str = Body(""),
):
    try:
        repo = g.get_repo(repo_name)
        base_branch = base_branch or repo.default_branch

        title = title or "Sweep AI Pull Request"

        new_branch = create_branch_and_push_changes(
            repo=repo,
            repo_name=repo_name,
            access_token=access_token,
            branch=branch,
            file_changes=file_changes,
            base_branch=base_branch,
            title=title,
        )
        pull_request = repo.create_pull(
            title=title,
            body=body,
            head=new_branch,
            base=base_branch,
        )
        with suppress_with_warning(Exception):
            if username:
                pull_request.add_to_assignees(username)
        file_diffs = pull_request.get_files()
        return {
            "pull_request": {
                "html_url": pull_request.html_url,
                "number": pull_request.number,
                "repo_name": repo_name,
                "title": title,
                "body": body,
                "labels": [],
                "status": "open",
                "sha": pull_request.head.sha,
                "file_diffs": [
                    {
                        "sha": file.sha,
                        "filename": file.filename,
                        "status": file.status,
                        "additions": file.additions,
                        "deletions": file.deletions,
                        "changes": file.changes,
                        "blob_url": file.blob_url,
                        "raw_url": file.raw_url,
                        "contents_url": file.contents_url,
                        "patch": file.patch,
                        "previous_filename": file.previous_filename,
                    }
                    for file in file_diffs
                ],
            },
            "new_branch": new_branch,
        }
    except GithubException as ge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub API error: {ge.data.get('message', str(ge))}",
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input: {str(ve)}")


@app.post("/create_pull_metadata")
@endpoint_wrapper
def create_pull_metadata(
    repo_name: str = Body(...),
    modify_files_dict: dict = Body(...),
    messages: list[Message] = Body(...),
    g: CustomGithub = Depends(get_github_client),
    repo: Repository = Depends(get_repo),
    original_issue: str = "",
):
    pr_template_string = ""
    pr_template_locations = [
        "pull_request_template.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/pull_request_template.md",
    ]
    for pr_template_location in pr_template_locations:
        try:
            pr_template_string = repo.get_contents(pr_template_location).decoded_content.decode("utf-8")
            break
        except Exception:
            continue
    new_modify_files_dict = FileModificationState()
    for file_path, file_content in modify_files_dict.items():
        new_modify_files_dict.add_or_update_file(file_path, file_content["original_contents"], file_content["contents"])

    title, description = get_pr_summary_for_chat(
        repo_name=repo_name,
        modify_files_dict=new_modify_files_dict,
        pr_template_string=pr_template_string,
    )

    # insert this before # Description if exists, otherwise insert this before the second markdown header "# ", otherwise append at the end
    formatted_original_issue = (
        f"This pull request was created to solve the following GitHub issue: <details>\n{original_issue}\n</details>"
    )
    if "# Description" in description:
        description = description.replace("# Description", f"{formatted_original_issue}\n\n# Description", 1)
    elif description.count("# ") >= 2:
        description = (
            description.split("# ", 2)[0]
            + f"{formatted_original_issue}\n\n# Description"
            + description.split("# ", 2)[1]
        )
    else:
        description += f"\n\n{formatted_original_issue}"

    if not title or not description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No title or description were generated for the pull request. Try again in a few seconds.",
        )

    commit_message = get_commit_message_for_diff(modify_files_dict=new_modify_files_dict)

    return {
        "success": True,
        "title": title,
        "description": description,
        "commit_message": commit_message,
        "branch": "sweep/" + clean_branch_name(title),
    }


@app.post("/validate_pull")
@endpoint_wrapper
async def validate_pull(
    repo_name: str = Body(...),
    pull_request_number: int = Body(...),
    file_changes: dict = Body({}),
    access_token: str = Depends(get_token_header),
    repo: Repository = Depends(get_repo),
):
    org_name, repo_name_ = repo_name.split("/")
    pull_request = repo.get_pull(int(pull_request_number))
    current_commit = pull_request.head.sha

    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_name, branch=pull_request.head.ref)
    for file_path, file_contents in file_changes.items():
        with open(os.path.join(cloned_repo.repo_dir, file_path), "w") as file:
            file.write(file_contents)
    installation_id = get_installation_id(org_name)

    async def stream():
        try:
            all_statuses: list[CheckStatus] = []
            docker_statuses: list[CheckStatus] = []
            for docker_statuses, file_changes in get_failing_docker_logs.stream(cloned_repo):
                yield json.dumps(docker_statuses)
            any_failed = not all_statuses or any(status["succeeded"] is False for status in docker_statuses)
            if not any_failed:
                for _ in range(60 * 6):
                    runs = list(repo.get_commit(current_commit).get_check_runs())
                    suite_runs = list(
                        repo.get_workflow_runs(branch=pull_request.head.ref, head_sha=pull_request.head.sha)
                    )
                    suite_statuses: list[CheckStatus] = [
                        {
                            "message": gha_to_message[run.status],
                            "stdout": "",  # TODO, fill this in
                            "succeeded": gha_to_check_status[run.status],
                            "status": gha_to_check_status[run.status],
                            "llm_message": "",
                            "container_name": run.name,
                        }
                        for run in sorted(suite_runs, key=lambda run: run.name)
                    ]
                    yield json.dumps(docker_statuses + suite_statuses)
                    if all(
                        [
                            run.conclusion in ["success", "skipped", None]
                            and run.status
                            not in [
                                "in_progress",
                                "waiting",
                                "pending",
                                "requested",
                                "queued",
                            ]
                            for run in runs
                        ]
                    ):
                        logger.info("All Github Actions have succeeded or have no result.")
                        break
                    if not any([run.conclusion == "failure" for run in runs]):
                        time.sleep(10)
                        continue
                    for i, run in enumerate(sorted(suite_runs, key=lambda run: run.name)):
                        if run.conclusion == "failure":
                            failed_logs = get_failing_gha_logs(
                                [run],
                                installation_id,
                            )
                            suite_statuses[i]["stdout"] = failed_logs
                            suite_statuses[i]["succeeded"] = False
                            suite_statuses[i]["status"] = "failure"
                            suite_statuses[i]["llm_message"] = failed_logs
                            yield json.dumps(docker_statuses + suite_statuses)
                    logger.info("Github Actions failed!")
                    break
        except Exception as e:
            logger.error(f"Error during streaming: {str(e)}")
            yield json.dumps(
                {
                    "status": "error",
                    "error": str(e),
                    "traceback": str(traceback.format_exc()),
                }
            )

    return StreamingResponseWithHeartbeat(stream())


@app.post("/validate_changes")
@endpoint_wrapper
def validate_changes(
    file_changes: dict = Body(...),
    cloned_repo: MockClonedRepo = Depends(get_cloned_repo),
):
    def stream():
        nonlocal file_changes
        try:
            docker_statuses: list[CheckStatus] = []
            for docker_statuses, file_changes in get_failing_docker_logs.stream(cloned_repo, file_changes):
                yield json.dumps(
                    {
                        "statuses": docker_statuses,
                        "file_changes": file_changes,
                    }
                )
            if not docker_statuses:
                yield json.dumps(
                    {
                        "status": "error",
                        "error": "No CI to run for the edited files.",  # TODO: improve this error message
                    }
                )
        except Exception as e:
            logger.error(f"Docker validation error: {str(e)}")
            yield json.dumps(
                {
                    "status": "error",
                    "error": f"Docker validation error: {str(e)}",
                    "traceback": str(traceback.format_exc()),
                }
            )

    return StreamingResponseWithHeartbeat(stream())


@app.get("/telemetry")
@endpoint_wrapper
def get_telemetry(_: bool = Depends(is_admin)):
    from pandas import read_csv

    try:
        events = read_posthog_events_from_disk()
        csv_text = format_posthog_events_as_csv(events)
        # write this to a file
        with open(f"{CACHE_DIRECTORY}/telemetry.csv", "w") as file:
            file.write(csv_text)
        df = read_csv(f"{CACHE_DIRECTORY}/telemetry.csv")
        # turn this to a dict
        result_dict = df.to_dict(orient="records")
        return result_dict
    except Exception as e:
        logger.error(f"Error getting telemetry data: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating telemetry data: {str(e)}")


@app.post("/messages/save")
@endpoint_wrapper
def write_message_to_disk(
    repo_name: str = Body(...),
    messages: list[Message] = Body(...),
    snippets: list[Snippet] = Body(...),
    code_suggestions: list = Body([]),
    pull_request: dict | None = Body(None),
    pull_request_title: str = Body(""),
    pull_request_body: str = Body(""),
    message_id: str = Body(""),
    user_mentioned_pull_request: dict | None = Body(None),
    user_mentioned_pull_requests: list[dict] | None = Body(None),
    commit_to_pr: str = Body("false"),
    fork_message: str = Body("test"),
    timestamp: float = Body(...),
    applied_changes: list[dict] = Body([]),
    pr_validation_statuses: list[dict] = Body([]),
    code_suggestions_state: str = Body("staging"),
    username: str = Body(""),
    branch: str = Body(""),
    feature_branch: str = Body(""),
    finished_creating_branch: bool = Body(False),
    g: CustomGithub = Depends(get_github_client),
):
    if not message_id or fork_message == "true":
        message_id = str(uuid.uuid4())
    if message_id.startswith("TEST_"):
        return {
            "status": "success",
            "message": "Message skipped for tests.",
            "message_id": message_id,
        }
    try:
        data = {
            "repo_name": repo_name,
            "branch": branch,
            "feature_branch": feature_branch,
            "messages": [message.model_dump() for message in messages],
            "snippets": [snippet.model_dump() for snippet in snippets],
            "code_suggestions": [
                (code_suggestion.__dict__ if isinstance(code_suggestion, CodeSuggestion) else code_suggestion)
                for code_suggestion in code_suggestions
            ],
            "pull_request": pull_request,
            "user_mentioned_pull_request": user_mentioned_pull_request,
            "user_mentioned_pull_requests": user_mentioned_pull_requests,
            "pull_request_title": pull_request_title,
            "pull_request_body": pull_request_body,
            "commit_to_pr": commit_to_pr,
            "timestamp": timestamp,
            "applied_changes": applied_changes,
            "pr_validation_statuses": pr_validation_statuses,
            "code_suggestions_state": code_suggestions_state,
            "username": username,
            "finishedCreatingBranch": finished_creating_branch,
            "updated_at": datetime.now().isoformat(),
        }
        with open(f"{CACHE_DIRECTORY}/messages/{message_id}.json", "w") as file:
            json.dump(data, file)
        logger.info(
            f"Saved {len(messages)} messages to {message_id}.json with timestamp {timestamp} and username {username}"
        )
        return {
            "status": "success",
            "message": "Message written to disk successfully.",
            "message_id": message_id,
        }
    except Exception as e:
        logger.error(f"Failed to write message to disk: {str(e)}")
        return {"status": "error", "error": "Failed to write message to disk."}


@app.get("/messages/load/{message_id}")
@endpoint_wrapper
def read_message_from_disk(
    message_id: str,
    last_timestamp: float = Query(0.0),
    access_token: str = Depends(get_token_header),
):
    try:
        with open(f"{CACHE_DIRECTORY}/messages/{message_id}.json", "r") as file:
            message_data = json.load(file)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Messages not found.")
    except Exception as e:
        logger.error(f"Failed to read message from disk: {str(e)}")
        posthog.capture(
            "sweep_chat_load error",
            "sweep_chat_load error",
            properties={
                "error": str(e),
                "message_id": message_id,
                "last_timestamp": last_timestamp,
            },
        )
        raise HTTPException(status_code=500, detail=f"Failed to read message from disk. {str(e)}")
    
    try:
        repo_name = message_data["repo_name"]
        get_github_client(repo_name, access_token)

        if message_data.get("timestamp", 0) >= last_timestamp:
            logger.info(
                f"Loaded {len(message_data['messages'])} messages from {message_id}.json with user {message_data.get('username', '')} and timestamp {message_data.get('timestamp', 0)}"
            )
            return {
                "status": "success",
                "message": "Message read from disk successfully.",
                "data": message_data,
            }
        else:
            return {"status": "no_update", "message": "No new updates available."}
    except Exception as e:
        if "credentials" in str(e):
            raise HTTPException(status_code=401, detail=f"Authorization error. {str(e)}")
        raise

@app.post("/messages/{message_id}/changes")
@endpoint_wrapper
def write_message_changes(
    message_id: str,
    applied_changes: list[dict] = Body(...),
    access_token: str = Depends(get_token_header),
):
    with open(f"{CACHE_DIRECTORY}/messages/{message_id}.json", "r") as file:
        message_data = json.load(file)
    message_data["applied_changes"] = applied_changes
    message_data["updated_at"] = datetime.now().isoformat()
    with open(f"{CACHE_DIRECTORY}/messages/{message_id}.json", "w") as file:
        json.dump(message_data, file)
    return {"status": "success", "message": "Applied changes written to disk successfully.", "updated_at": message_data["updated_at"]}

@app.get("/messages/{message_id}/changes")
@endpoint_wrapper
def read_message_changes(message_id: str, access_token: str = Depends(get_token_header)):
    with open(f"{CACHE_DIRECTORY}/messages/{message_id}.json", "r") as file:
        message_data = json.load(file)
    return message_data["applied_changes"]

@app.get("/get_chat_owner/{message_id}")
@endpoint_wrapper
async def get_chat_owner(message_id: str, access_token: str = Depends(get_token_header)):
    try:
        with open(f"{CACHE_DIRECTORY}/messages/{message_id}.json", "r") as file:
            message_data = json.load(file)
        if "username" in message_data:
            return {"username": message_data["username"]}
        else:
            return {"username": ""}
    except FileNotFoundError:
        logger.error(f"Chat was not found: {message_id}")
        return {"username": ""}
    except Exception as e:
        logger.error(f"Failed to get chat owner: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get chat owner. {str(e)}")


# TODO: pass in cloned repo
async def fix_issue(
    repo_full_name: str,
    query: str,
    access_token: str,
    messages: list[Message] = [],
    snippets: list = [],
    branch: str = None,
    username: str = "",
    pulls: list[dict] = [],
    context: ChatAgentContext = ChatAgentContext(),
) -> FixIssueResult:  # type: ignore
    g = get_github(repo_full_name)
    messages = messages or [UserMessage(content=query)]
    username = username or Github(access_token, base_url=GITHUB_API_BASE_URL).get_user().login
    snippets = [snippet if isinstance(snippet, Snippet) else Snippet(**snippet) for snippet in snippets]

    annotations = {} if not pulls else {"pulls": pulls}
    if annotations and (first_message := next((message for message in messages if message.role == "user"), None)):
        first_message.annotations = first_message.annotations or {}
        first_message.annotations.update(annotations)
    
    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name=repo_full_name, branch=branch)
    if not snippets and annotations:
        snippets, _, _ = get_pr_snippets(
            repo_full_name,
            annotations,
            cloned_repo,
            context=context,
        )

    # Step 1: Call agentic_search_codebase_endpoint
    _message, snippets, new_messages = wrapped_file_searcher(
        cloned_repo=cloned_repo,
        query=query,
        messages=messages,
        existing_snippets=snippets,
        username=username,
        annotations=annotations,
        context=context,
    )

    for message in new_messages:
        message.role = "function"
        if message.function_call is not None:
            message.function_call["is_complete"] = True

    messages = messages + new_messages

    # Step 3: Call chat_codebase
    code_entity_relationship_map, search_agent_solution, existing_patterns, messages = preprocess_messages(messages)
    new_messages = chat_agent(
        username,
        cloned_repo,
        deepcopy(messages),
        modify_files_dict={},
        snippets=snippets,
        metadata={
            "repo_name": repo_full_name,
            "message": query,
            "messages": [message.model_dump() for message in messages],
            "snippets": [snippet.model_dump() for snippet in snippets],
            "code_entity_relationship_map": code_entity_relationship_map,
            "search_agent_solution": search_agent_solution,
            "existing_patterns": existing_patterns,
        },
        context=context,
    )
    messages = messages + new_messages

    code_suggestions = messages[-1].annotations["codeSuggestions"]
    new_branch = ""

    # DEBUGGING DATA START
    # import random
    # code_suggestions = [
    #     {
    #         "filePath": "sweepai/test.py", # add sweepai in path to run ci
    #         "originalCode": "",
    #         "newCode": "def test():\n    return test" + str(random.randint(0, 1000000)) + "'"
    #     }
    # ]
    # messages = [
    #     Message(
    #         content="Testing",
    #         role="user"
    #     )
    # ]
    # DEBUGGING DATA END

    pull_request_data = None
    if code_suggestions:
        file_changes = {suggestion["filePath"]: suggestion["newCode"] for suggestion in code_suggestions}
        modify_files_dict = {
            suggestion["filePath"]: {
                "original_contents": suggestion["originalCode"],
                "contents": suggestion["newCode"],
            }
            for suggestion in code_suggestions
        }

        if len(pulls) > 0:
            # commit to branch
            new_modify_files_dict = FileModificationState()
            for file_path, file_content in modify_files_dict.items():
                new_modify_files_dict.add_or_update_file(
                    file_path,
                    file_content["original_contents"],
                    file_content["contents"],
                )
            commit_message = get_commit_message_for_diff(modify_files_dict=new_modify_files_dict)
            repo = cloned_repo.github_repo
            await commit_to_branch(
                repo_name=repo_full_name,
                file_changes=file_changes,
                base_branch=branch,
                branch=branch,
                commit_message=commit_message,
                access_token=access_token,
                g=g,
                repo=repo,
            )
            pull = pulls[0]
            pull_request = repo.get_pull(pull["number"])
            pull_request_data = PullRequestData(
                number=pull_request.number,
                html_url=pull_request.html_url,
                title=pull_request.title,
                body=pull_request.body,
                sha=pull_request.head.sha,
            )
            pr_response = {}
            pr_metadata = {}
            commit = pull_request.get_commits()[0]
            messages.append(
                AssistantMessage(
                    content=f"Changes committed to branch via {hyperlink(commit.sha[:7], commit.html_url)}",
                )
            )
        else:
            pr_metadata = create_pull_metadata(
                repo_name=repo_full_name,
                modify_files_dict=modify_files_dict,
                messages=messages,
                g=g,
                repo=g.get_repo(repo_full_name),
                original_issue=query,
            )

            pr_response = create_pull(
                repo_name=repo_full_name,
                file_changes=file_changes,
                branch=pr_metadata["branch"],
                title=pr_metadata["title"],
                body=pr_metadata["description"],
                base_branch=branch,
                access_token=access_token,
                g=g,
                username=username,
            )

            new_branch = pr_response["new_branch"]

            pull_request = pr_response["pull_request"]
            pr_url = pull_request["html_url"]

            messages.append(
                AssistantMessage(
                    content=f"Pull request created: {pr_url}",
                    annotations={
                        "pulls": [
                            {
                                "number": pull_request["number"],
                                "repo_name": pull_request["repo_name"],
                                "title": pull_request["title"],
                                "body": pull_request["body"],
                                "labels": pull_request["labels"],
                                "status": pull_request["status"],
                                "file_diffs": pull_request["file_diffs"],
                                "branch": new_branch,
                            }
                        ]
                    },
                )
            )
            pull_request_data = PullRequestData(
                number=pull_request["number"],
                html_url=pull_request["html_url"],
                title=pull_request["title"],
                body=pull_request["body"],
                sha=pull_request["sha"],
            )
    else:
        file_changes = {}
        pr_response = {}
        pr_metadata = {}

    # NOTE: When calling fastapi endpoints without code,
    # the default params are not passed along so you must manually add them.
    # When calling the function directly, you're bypassing all of FastAPI's HTTP-related functionality, including request validation, response modeling,
    # and automatic documentation generation.
    write_message_to_disk_default_params = {
        "message_id": None,
        "user_mentioned_pull_request": None,  # this should be set for on_comment by checking interface PullRequest (not sure if this affects functionality)
        "user_mentioned_pull_requests": None,  # same as above
        "commit_to_pr": "false",
        "fork_message": "false",
        "timestamp": time.time(),
        "pr_validation_statuses": [],
        "code_suggestions_state": "staging",
        "finished_creating_branch": True,
    }

    write_results = write_message_to_disk(
        repo_name=repo_full_name,
        messages=messages,
        snippets=snippets,
        code_suggestions=code_suggestions,
        pull_request=pr_response.get("pull_request"),
        pull_request_title=pr_metadata.get("title"),
        pull_request_body=pr_metadata.get("description"),
        applied_changes=[],
        username=username,
        branch=branch,
        feature_branch=new_branch,
        **write_message_to_disk_default_params,
    )
    if "message_id" in write_results:
        messages_id = write_results["message_id"]
    else:
        logger.error(f"No message id found while writing to disk for {repo_full_name}")
        messages_id = "MESSAGE_ID_NOT_FOUND"

    return FixIssueResult(
        snippets=snippets,
        messages=messages,
        changes=file_changes,
        pull_request_data=pull_request_data,
        messages_id=messages_id,
        frontend_url=f"{FRONTEND_URL}/c/{messages_id}",
    )


if __name__ == "__main__":
    import fastapi.testclient

    client = fastapi.testclient.TestClient(app)
    # response = client.get("/search?repo_name=sweepai/sweep&query=backend")
    # print(response.text)
    messages = [Message(content="Where is the backend code?", role="user")]
    snippets = [
        Snippet(
            content="def get_backend():\n    return 'backend'",
            file_path="backend.py",
            start=0,
            end=1,
        )
    ]
    response = client.post(
        "/chat",
        json={
            "repo_name": "sweepai/sweep",
            "messages": [message.model_dump() for message in messages],
            "snippets": [snippet.model_dump() for snippet in snippets],
        },
    )
    print(response.text)
