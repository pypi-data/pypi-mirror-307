from contextlib import suppress
from urllib.parse import urlparse

from pydantic import BaseModel

class GitHubRepoURL(BaseModel):
    org_name: str
    repo_name: str

    @property
    def repo_full_name(self) -> str:
        return f"{self.org_name}/{self.repo_name}"

class CommentURL(GitHubRepoURL):
    pull_request_number: int
    comment_id: int
    is_review_comment: bool = False

    @classmethod
    def parse_from_url(cls, url: str):
        # e.g. https://github.com/org/repo/pull/999/files#r1234567890
        # e.g. https://github.com/org/repo/pull/999#discussion_r1234567890
        # e.g. https://github.com/org/repo/pull/999#issuecomment-1234567890
        if (
            "#issuecomment-" not in url
            and "#discussion_r" not in url
            and "#r" not in url
            and "#issuecomment-" not in url
        ):
            raise ValueError("Not a comment")
        parsed_url = urlparse(url)
        org_name, repo_name, _, pull_request_number, *_ = parsed_url.path.strip("/").split("/")
        comment_id = parsed_url.fragment.removeprefix("issuecomment-").removeprefix("discussion_r").removeprefix("r")
        is_review_comment = "#discussion_r" in url or "#r" in url
        return cls(
            org_name=org_name,
            repo_name=repo_name,
            pull_request_number=pull_request_number,
            comment_id=comment_id,
            is_review_comment=is_review_comment,
        )


class PullRequestURL(GitHubRepoURL):
    pull_request_number: int

    @classmethod
    def parse_from_url(cls, url: str):
        # e.g. https://github.com/org/repo/pull/999
        parsed_url = urlparse(url)
        org_name, repo_name, type_name, pull_request_number, *_files = parsed_url.path.strip("/").split("/")
        if type_name != "pull":
            raise ValueError("Not a pull request")
        return cls(
            org_name=org_name,
            repo_name=repo_name,
            pull_request_number=pull_request_number,
        )


class IssueURL(GitHubRepoURL):
    issue_number: int

    @classmethod
    def parse_from_url(cls, url: str):
        # e.g. https://github.com/org/repo/issues/999
        parsed_url = urlparse(url)
        org_name, repo_name, type_name, issue_number = parsed_url.path.strip("/").split("/")
        if type_name != "issues":
            raise ValueError("Not an issue")
        return cls(org_name=org_name, repo_name=repo_name, issue_number=issue_number)


def parse_url(url: str) -> IssueURL | CommentURL | PullRequestURL:
    for cls in [CommentURL, PullRequestURL, IssueURL]:
        with suppress(ValueError):
            return cls.parse_from_url(url)
    raise ValueError("Not an issue, comment or pull request")
