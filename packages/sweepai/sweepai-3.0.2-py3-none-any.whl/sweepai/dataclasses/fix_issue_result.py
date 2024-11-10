from dataclasses import dataclass

from sweepai.core.entities import Message, Snippet


@dataclass
class PullRequestData:
    number: int
    html_url: str
    title: str
    body: str
    sha: str


@dataclass
class FixIssueResult:
    snippets: list[Snippet]
    messages: list[Message]
    changes: dict[str, str]
    pull_request_data: PullRequestData | None
    messages_id: str
    frontend_url: str
