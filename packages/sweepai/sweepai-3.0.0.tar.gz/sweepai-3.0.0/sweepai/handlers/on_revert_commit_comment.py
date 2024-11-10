from github.Commit import Commit
from github.GithubException import GithubException
from github.InputGitTreeElement import InputGitTreeElement
from loguru import logger

from sweepai.config.server import GITHUB_BASE_URL
from sweepai.core.github_utils import github_integration
from sweepai.o11y.log_utils import log_to_file, log_warnings_to_file
from sweepai.utils.file_utils import safe_decode
from sweepai.utils.ticket_rendering_utils import (
    PR_REVERTED_INDICATOR,
    create_or_edit_sweeps_github_comment,
)
from sweepai.web.events import CommentCreatedOrEditedRequest, IssueCommentRequest


def extract_pr_and_commit_from_comment(original_line_to_revert: str) -> tuple[int, str]:
    # Expects the entire comment
    split_original_line = original_line_to_revert.split(PR_REVERTED_INDICATOR)[-1].split(f"](https://{GITHUB_BASE_URL}")
    assert len(split_original_line) >= 2 and isinstance(
        split_original_line[1], str
    ), f"Invalid first half of comment: {original_line_to_revert}"
    pr_url = split_original_line[1].split(")")[0]
    # index from the end to be safer
    split_pr_url = pr_url.split("/")
    assert (
        len(split_pr_url) > 2 and isinstance(split_pr_url[-1], str) and isinstance(split_pr_url[-2], str)
    ), f"Invalid PR Url/second half of comment: {split_pr_url}"
    pr_number = split_pr_url[-3]
    commit_sha = split_pr_url[-1]
    assert pr_number.isdigit() and isinstance(
        commit_sha, str
    ), f"Invalid PR number or commit SHA: {pr_number}, {commit_sha}"
    return int(pr_number), commit_sha


def create_commit_name_for_revert(commit_to_revert: Commit) -> str:
    # Create the revert commit
    # truncate message accounting 50 character limit + length of other text (which is 43 from "revert " (7)
    safe_length_message = (
        commit_to_revert.commit.message
        if len(commit_to_revert.commit.message) < 43
        else commit_to_revert.commit.message[: commit_to_revert.commit.message.rfind(" ", 0, 43)]
    )
    commit_message = f"Revert {safe_length_message}"
    assert len(commit_message) <= 50, "Commit message too long"
    return commit_message


def on_revert_commit_comment(
    issue_comment_request: IssueCommentRequest | CommentCreatedOrEditedRequest,
    tracking_id: str,
):
    with log_to_file(tracking_id), log_warnings_to_file(keywords=["[YELLOW]"], tracking_id=tracking_id):
        original_comment_id = issue_comment_request.comment.id
        current_body = issue_comment_request.comment.body
        repo_full_name = issue_comment_request.repository.full_name
        org_name, repo_name = repo_full_name.split("/")
        installation = github_integration.get_repo_installation(org_name, repo_name)
        repo = installation.get_github_for_installation().get_repo(repo_full_name)
        pr_number, commit_sha = extract_pr_and_commit_from_comment(current_body)
        pull_request = repo.get_pull(pr_number)

        if isinstance(issue_comment_request, CommentCreatedOrEditedRequest):
            all_comments = pull_request.get_review_comments()
        else:
            all_comments = pull_request.get_issue_comments()

        sweeps_github_comment = None
        for comment in all_comments:
            if comment.id == original_comment_id:
                sweeps_github_comment = comment
                break
        sweeps_github_comment = create_or_edit_sweeps_github_comment(
            issue_or_pr=pull_request,
            sweeps_message=f"I'm reverting #{pr_number}...",
            sweeps_github_comment=sweeps_github_comment,
            tracking_id=tracking_id,
        )

        commit_to_revert = repo.get_commit(commit_sha)

        # check no other commits have been pushed to the branch since the PR was created
        if commit_sha != pull_request.head.sha:
            logger.info(
                f"More commits have been pushed to the branch since the PR was created. Not reverting {commit_sha}."
            )
            return

        head_branch = pull_request.head.ref

        try:
            # Get the diff of the commit to revert
            diff = commit_to_revert.files

            commit_before_commit_to_revert = commit_to_revert.parents[0]

            # Create dictionaries to store the current state of the tree, file modes, and contents
            current_tree = {}
            file_contents = {}

            for file_to_revert in commit_to_revert.files:
                current_tree[file_to_revert.filename] = file_to_revert.sha

            # Apply the inverse changes to the current_tree dictionary
            for file in diff:
                if file.status == "added":
                    # If file was added, we'll delete it
                    continue
                elif file.status == "removed":
                    # If file was removed, we'll add it back
                    content = (
                        safe_decode(
                            repo=repo,
                            path=file.filename,
                            ref=commit_before_commit_to_revert.sha,
                        )
                        or ""
                    )
                    if content is not None:
                        current_tree[file.filename] = file.filename
                        file_contents[file.filename] = content
                elif file.status == "modified":
                    # If file was modified, we'll revert to the previous version
                    content = (
                        safe_decode(
                            repo=repo,
                            path=file.filename,
                            ref=commit_before_commit_to_revert.sha,
                        )
                        or ""
                    )
                    if content is not None:
                        current_tree[file.filename] = file.filename
                        file_contents[file.filename] = content
                elif file.status == "renamed":
                    # If file was renamed, we'll move it back
                    content = (
                        safe_decode(
                            repo=repo,
                            path=file.previous_filename,
                            ref=commit_before_commit_to_revert.sha,
                        )
                        or ""
                    )
                    if content is not None:
                        current_tree[file.previous_filename] = file.previous_filename
                        file_contents[file.previous_filename] = content

            # Create the list of InputGitTreeElements
            tree_elements = [
                InputGitTreeElement(path=path, mode="100644", type="blob", content=file_contents[path])
                for path in current_tree.keys()
            ]

            # Create a new tree with the inverse changes
            new_tree = repo.create_git_tree(tree_elements, base_tree=repo.get_git_tree(sha=pull_request.head.sha))

            # Create the revert commit
            commit_message = create_commit_name_for_revert(commit_to_revert)
            revert_commit = repo.create_git_commit(
                message=commit_message,
                tree=new_tree,
                parents=[repo.get_git_commit(sha=pull_request.head.sha)],
            )

            # Update the branch reference
            ref = repo.get_git_ref(f"heads/{head_branch}")
            ref.edit(sha=revert_commit.sha)

            logger.info(f"Successfully created revert commit on branch {head_branch}")

            successful_revert_message = f"I've reverted commit {revert_commit.sha} on branch `{head_branch}`. "
            sweeps_github_comment = create_or_edit_sweeps_github_comment(
                issue_or_pr=pull_request,
                sweeps_message=successful_revert_message,
                sweeps_github_comment=sweeps_github_comment,
                tracking_id=tracking_id,
            )
        except GithubException as e:
            logger.error(f"GitHub API error while creating revert commit: {str(e)}")
            sweeps_github_comment = create_or_edit_sweeps_github_comment(
                issue_or_pr=pull_request,
                sweeps_message=f"I failed to create a revert commit. GitHub API Error: {str(e)}",
                sweeps_github_comment=sweeps_github_comment,
                tracking_id=tracking_id,
            )
        except Exception as e:
            logger.error(f"Error while creating revert commit: {str(e)}")
            sweeps_github_comment = create_or_edit_sweeps_github_comment(
                issue_or_pr=pull_request,
                sweeps_message=f"I failed to create a revert commit. Error: {str(e)}",
                sweeps_github_comment=sweeps_github_comment,
                tracking_id=tracking_id,
            )
