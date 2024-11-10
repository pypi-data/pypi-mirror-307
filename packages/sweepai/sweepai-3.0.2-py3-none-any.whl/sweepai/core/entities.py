from __future__ import annotations

import os
import re
from difflib import unified_diff
from typing import Any, ClassVar, Literal, Type, TypeVar

from loguru import logger
from pydantic import BaseModel, Field

from sweepai.utils.diff import generate_diff
from sweepai.utils.str_utils import (
    add_line_numbers,
    blockquote,
    rstrip_lines,
    strip_triple_quotes,
)

Self = TypeVar("Self", bound="RegexMatchableBaseModel")


# pylint: disable=no-member,unsubscriptable-object
class Message(BaseModel):
    role: Literal["system"] | Literal["user"] | Literal["assistant"] | Literal["function"]
    content: str | None = None
    name: str | None = None
    function_call: dict | None = None
    key: str | None = None
    annotations: dict | None = None

    @classmethod
    def from_tuple(cls, tup: tuple[str | None, str | None]) -> Self:
        if tup[0] is None:
            return cls(role="assistant", content=tup[1])
        else:
            return cls(role="user", content=tup[0])

    def to_openai(self) -> str:
        obj = {
            "role": self.role,
            "content": self.content,
        }
        if self.function_call:
            obj["function_call"] = self.function_call
        if self.role == "function":
            obj["name"] = self.name
        return obj

    def __repr__(self):
        # take the first 100 and last 100 characters of the message if it's too long
        if self.content is None:
            return "No content."
        truncated_message_content = (
            self.content[:100] + "..." + self.content[-100:] if len(self.content) > 200 else self.content
        )
        return f"\nSTART OF MESSAGE\n\n{truncated_message_content}\n\nROLE: {self.role} FUNCTION_CALL: {self.function_call} NAME: {self.name} ANNOTATIONS: {self.annotations if self.annotations else ''} KEY: {self.key}\n\nEND OF MESSAGE\n\n"


class SystemMessage(Message):
    role: Literal["system"] = "system"
    key: str = "system"


class UserMessage(Message):
    role: Literal["user"] = "user"


class AssistantMessage(Message):
    role: Literal["assistant"] = "assistant"


class FunctionMessage(Message):
    role: Literal["function"] = "function"


class Function(BaseModel):
    class Parameters(BaseModel):
        type: str = "object"
        properties: dict

    name: str
    description: str
    parameters: Parameters


class RegexMatchError(ValueError):
    pass


class RegexMatchableBaseModel(BaseModel):
    _regex: ClassVar[str]

    @classmethod
    def from_string(cls: Type[Self], string: str, **kwargs) -> Self:
        # match = re.search(file_regex, string, re.DOTALL)
        match = re.search(cls._regex, string, re.DOTALL)
        if match is None:
            logger.warning(f"Did not match {string} with pattern {cls._regex}")
            raise RegexMatchError("Did not match")
        return cls(
            **{k: (v if v else "").strip("\n") for k, v in match.groupdict().items()},
            **kwargs,
        )


class FileChangeRequest(RegexMatchableBaseModel):
    filename: str
    instructions: str
    change_type: (
        Literal["modify"]
        | Literal["create"]
        | Literal["delete"]
        | Literal["rename"]
        | Literal["rewrite"]
        | Literal["check"]
        | Literal["refactor"]
        | Literal["test"]
    )
    _regex = r"""<(?P<change_type>[a-z_]+)\s+file=\"(?P<filename>[a-zA-Z0-9/\\\.\[\]\(\)\_\+\- @\{\}]*?)\"( start_line=\"(?P<start_line>.*?)\")?( end_line=\"(?P<end_line>.*?)\")?( entity=\"(.*?)\")?( source_file=\"(?P<source_file>.*?)\")?( destination_module=\"(?P<destination_module>.*?)\")?( relevant_files=\"(?P<raw_relevant_files>.*?)\")?(.*?)>(?P<instructions>.*?)\s*<\/\1>"""
    is_completed: bool = False
    entity: str | None = None
    source_file: str | None = None
    old_content: str | None = None
    new_content: str | None = None
    raw_relevant_files: str | None = None
    # allow inf
    start_line: Any | int | str | None = None
    end_line: Any | int | str | None = None
    start_and_end_lines: list[tuple] = []
    comment_line: int | None = None
    sandbox_response: None = None
    failed_sandbox_test: bool | None = False
    parent: FileChangeRequest | None = None
    status: Literal["succeeded"] | Literal["failed"] | Literal["queued"] | Literal["running"] = "queued"
    destination_module: str | None = None
    commit_hash_url: str | None = None
    id: str | None = None

    def __repr__(self):
        return f"START OF FCR\n\n{self.change_type.capitalize()}: {self.filename} with instructions:\n{self.instructions}\n\nEND OF FCR\n\n"

    def get_edit_url(self, repo_full_name: str, branch_name: str):
        url = f"https://github.com/{repo_full_name}/edit/{branch_name}/{self.filename}"
        if self.start_line and self.end_line:
            url += f"#L{self.start_line}-L{self.end_line}"
        return url

    @classmethod
    def from_string(cls: Type[Self], string: str, **kwargs) -> Self:
        result = super().from_string(string, **kwargs)
        result.filename = result.filename.strip("/")
        result.instructions = result.instructions.replace("\n*", "\n•")
        if result.source_file:
            result.source_file = result.source_file.strip()
            if " " in result.source_file:
                result.source_file = result.source_file.split(" ")[0]
        if result.instructions.startswith("*"):
            result.instructions = "•" + result.instructions[1:]
        if result.start_line:
            try:
                result.start_line = int(result.start_line)
            except ValueError:
                result.start_line = None
        if result.end_line:
            try:
                result.end_line = int(result.end_line)
            except ValueError:
                result.start_line = None
        return result

    @property
    def relevant_files(self):
        if not self.raw_relevant_files:
            return []

        return [relevant_file for relevant_file in self.raw_relevant_files.split(" ") if relevant_file != self.filename]

    @property
    def entity_display(self):
        if self.entity:
            return f"`{self.filename}:{self.entity}`"
        else:
            return f"`{self.filename}`"

    @property
    def status_display(self):
        if self.status == "succeeded":
            return "✓"
        elif self.status == "failed":
            if self.change_type == "modify":
                return "! No changes made"
            return "✗"
        elif self.status == "queued":
            return "▶"
        elif self.status == "running":
            return "⋯"
        else:
            raise ValueError(f"Unknown status {self.status}")

    @property
    def display_summary(self):
        if self.change_type == "check":
            return f"Running GitHub Actions for `{self.filename}`"
        return f"{self.change_type.capitalize()} `{self.filename}`"

    @property
    def summary(self):
        prefix = {"failed": "✗", "succeeded": "✓", "queued": "▶", "running": "⋯"}[self.status] + " "
        return prefix + f"{self.change_type.capitalize()}\n{self.filename}"

    @property
    def color(self):
        color_map = {
            "failed": "red2",
            "succeeded": "#0ee832",
            "queued": "white",
            "running": "yellow",
        }
        return color_map[self.status]

    @property
    def entity_display_without_backtick(self):
        if self.entity:
            return f"{self.filename}:{self.entity}"
        else:
            return f"{self.filename}"

    @property
    def instructions_ticket_display(self):
        return self.instructions_display

    @property
    def instructions_display(self):
        # if self.change_type == "check":
        #     return f"Run GitHub Actions for `{self.filename}` with results:\n{self.instructions}"
        return f"{self.change_type.capitalize()} {self.filename} with contents:\n{self.instructions}"

    @property
    def diff_display(self):
        if self.old_content and self.new_content:
            diff = unified_diff(
                self.old_content.splitlines(keepends=True),
                self.new_content.splitlines(keepends=True),
            )
            diff_text = "".join(diff)
            return f"<pre>{diff_text}</pre>"
        return ""


class SweepPullRequest(RegexMatchableBaseModel):
    title: str
    branch_name: str
    content: str
    _regex = r'''pr_title\s+=\s+"(?P<title>.*?)"\n+branch\s+=\s+"(?P<branch_name>.*?)"\n+pr_content\s+=\s+f?"""(?P<content>.*?)"""'''


class ProposedIssue(RegexMatchableBaseModel):
    title: str
    body: str
    issue_id: int | None = None
    _regex = r'<issue\s+title="(?P<title>.*?)">(?P<body>.*?)</issue>'


SNIPPET_FORMAT = """<code_block>
<source>{denotation}</source>
<code_block_content>
{contents}
</code_block_content>
</code_block>"""


# pylint: disable=no-member,unsubscriptable-object
class Snippet(BaseModel):
    """
    Start and end refer to line numbers
    """

    content: str = Field(repr=False)
    start: int
    end: int
    file_path: str
    score: float = 0.0  # TODO: migrate all usages to use this
    type_name: Literal["source", "tests", "dependencies", "tools", "docs"] = "source"

    def __init__(self, **data):
        super().__init__(**data)
        self.start = max(1, self.start)

    def __eq__(self, other):
        if isinstance(other, Snippet):
            return self.file_path == other.file_path and self.start == other.start and self.end == other.end
        return False

    def __hash__(self):
        return hash((self.file_path, self.start, self.end))

    def __repr__(self):
        return f"{self.file_path}:{self.start}-{self.end}\n"

    def get_snippet(self, add_ellipsis: bool = True, add_lines: bool = True):
        if self.content is None:
            return ""
        lines = self.content.splitlines()
        snippet = "\n".join(lines[max(self.start - 1, 0) : self.end])

        if add_lines:
            snippet = add_line_numbers(snippet, start=self.start)

        if add_ellipsis:
            if self.start > 1:
                snippet = "...\n" + snippet
            if self.end < self.content.count("\n") + 1:
                snippet = snippet + "\n..."
        return snippet

    def __add__(self, other):
        assert self.content == other.content
        assert self.file_path == other.file_path
        return Snippet(
            content=self.content,
            start=self.start,
            end=other.end,
            file_path=self.file_path,
        )

    def __xor__(self, other: "Snippet") -> bool:
        """
        Returns True if there is an overlap between two snippets.
        """
        if self.file_path != other.file_path:
            return False
        return self.file_path == other.file_path and (
            (self.start <= other.start and self.end >= other.start)
            or (other.start <= self.start and other.end >= self.start)
        )

    def __or__(self, other: "Snippet") -> "Snippet":
        assert self.file_path == other.file_path
        return Snippet(
            content=self.content,
            start=min(self.start, other.start),
            end=max(self.end, other.end),
            file_path=self.file_path,
        )

    @property
    def xml(self):
        return SNIPPET_FORMAT.format(denotation=self.file_denotation, contents=self.get_snippet())

    def expand(self, num_lines: int = 25):
        return Snippet(
            content=self.content,
            start=max(self.start - num_lines, 1),
            end=min(self.end + num_lines, self.content.count("\n") + 1),
            file_path=self.file_path,
            score=self.score,
        )

    def render(self, i: int | None = None, EXPAND_SIZE: int = 100):
        headers = '<relevant_file index="' + str(i) + '">' if i is not None else "<relevant_file>"
        return f"""{headers}
<file_path>
{self.file_denotation}
</file_path>
<source>
{self.expand(EXPAND_SIZE).get_snippet(add_lines=False)}
</source>
</relevant_file>"""

    @property
    def denotation(self):
        return f"{self.file_path}:{self.start}-{self.end}"

    @property
    def file_denotation(self):
        if self.start <= 0 and self.end >= self.content.count("\n") + 1:
            return f"{self.file_path}"
        return f"{self.file_path}:{self.start}-{self.end}"

    @classmethod
    def from_file(cls, file_path: str, file_contents: str, **kwargs):
        return cls(
            content=file_contents,
            start=0,
            end=file_contents.count("\n"),
            file_path=file_path,
            **kwargs,
        )

def sort_and_fuse_snippets(
    snippets: list[Snippet],
    fuse_distance: int = 600,
) -> list[Snippet]:
    if len(snippets) <= 1:
        return snippets
    new_snippets = []
    snippets.sort(key=lambda x: x.start)
    current_snippet = snippets[0]
    for snippet in snippets[1:]:
        if current_snippet.end + fuse_distance >= snippet.start:
            current_snippet.end = max(current_snippet.end, snippet.end)
            current_snippet.score = max(current_snippet.score, snippet.score)
        else:
            new_snippets.append(current_snippet)
            current_snippet = snippet
    new_snippets.append(current_snippet)
    return new_snippets


def organize_snippets(snippets: list[Snippet], fuse_distance: int = 600) -> list[Snippet]:
    """
    Fuse and dedup snippets that are contiguous. Combine ones of same file.
    """
    fused_snippets = []
    added_file_paths = set()
    for i, snippet in enumerate(snippets):
        if snippet.file_path in added_file_paths:
            continue
        added_file_paths.add(snippet.file_path)
        current_snippets = [snippet]
        for current_snippet in snippets[i + 1 :]:
            if snippet.file_path == current_snippet.file_path:
                current_snippets.append(current_snippet)
        current_snippets = sort_and_fuse_snippets(current_snippets, fuse_distance=fuse_distance)
        fused_snippets.extend(current_snippets)
    return fused_snippets

def snippet_to_string(snippet: Snippet) -> str:
    return snippet.get_snippet(add_lines=False, add_ellipsis=False)


def fuse_snippets(snippets: list[Snippet]) -> list[Snippet]:
    """
    Fuses overlapping snippets into a single snippet.
    """
    new_snippets: list[Snippet] = []
    for snippet in snippets:
        for new_snippet in new_snippets:
            if new_snippet.file_path == snippet.file_path:
                if new_snippet.end + 1 == snippet.start:
                    new_snippet.end = snippet.end
                    break
                elif new_snippet.start - 1 == snippet.end:
                    new_snippet.start = snippet.start
                    break
        else:
            new_snippets.append(snippet)
    return new_snippets


class NoFilesException(Exception):
    def __init__(self, message="Sweep could not find any files to modify"):
        super().__init__(message)


class UnsuitableFileException(Exception):
    def __init__(self, message="Sweep has determined this file is unsuitable to work with"):
        super().__init__(message)


class PRChangeRequest(BaseModel):
    params: dict


class MockPR(BaseModel):
    # Used to mock a PR object without creating a PR (branch will be created tho)
    file_count: int = 0  # Number of files changes
    title: str
    body: str
    pr_head: str
    base: Any
    head: Any
    assignee: Any = None

    id: int = -1
    state: str = "open"
    html_url: str = ""

    def create_review(self, *args, **kwargs):
        # Todo: used to prevent erroring in on_review.py file
        pass

    def create_issue_comment(self, *args, **kwargs):
        pass


class SandboxResponse(BaseModel):
    success: bool
    outputs: list[str]
    updated_content: str
    error_messages: list[str]


class MaxTokensExceeded(Exception):
    def __init__(self, filename):
        self.filename = filename


class UnneededEditError(Exception):
    def __init__(self, filename):
        self.filename = filename


class MatchingError(Exception):
    def __init__(self, filename):
        self.filename = filename


class EmptyRepository(Exception):
    def __init__(self):
        pass


def parse_fcr(fcr: FileChangeRequest):
    justification, *_ = fcr.instructions.split("<original_code>", 1)
    justification, *_ = justification.split("<new_code>", 1)
    justification = (
        justification.rstrip().removesuffix("1.").removesuffix("2.").rstrip()
    )  # sometimes Claude puts 1. <original_code> which is weird
    original_code_pattern = r"<original_code(?: file_path=\".*?\")?(?: index=\"\d+\")?>\s*\n(.*?)</original_code>"
    new_code_pattern = r"<new_code(?: file_path=\".*?\")?(?: index=\"\d+\")?>\s*\n(.*?)</new_code>"
    original_code_matches = list(re.finditer(original_code_pattern, fcr.instructions, re.DOTALL))
    new_code_matches = list(re.finditer(new_code_pattern, fcr.instructions, re.DOTALL))
    replace_all_pattern = r"<replace_all>true</replace_all>"
    replace_all_matches = list(re.finditer(replace_all_pattern, fcr.instructions, re.DOTALL))
    return {
        "justification": justification.strip(),
        "file_path": fcr.filename,
        "original_code": [
            strip_triple_quotes(original_code_match.group(1)) for original_code_match in original_code_matches
        ],
        "new_code": [strip_triple_quotes(new_code_match.group(1)) for new_code_match in new_code_matches],
        "replace_all": bool(replace_all_matches),
    }


def render_fcrs(file_change_requests: list[FileChangeRequest]):
    # Render plan start
    planning_markdown = ""
    for fcr in file_change_requests:
        parsed_fcr = parse_fcr(fcr)
        if parsed_fcr and parsed_fcr["new_code"]:
            planning_markdown += f"#### `{fcr.filename}`\n"
            planning_markdown += f"{blockquote(parsed_fcr['justification'])}\n\n"
            if parsed_fcr["original_code"] and parsed_fcr["original_code"][0].strip():
                planning_markdown += f"""```diff\n{generate_diff(
                    parsed_fcr["original_code"][0],
                    rstrip_lines(parsed_fcr["new_code"][0]),
                )}\n```\n"""
            else:
                _file_base_name, ext = os.path.splitext(fcr.filename)
                planning_markdown += f"```{ext}\n{parsed_fcr['new_code'][0]}\n```\n"
        else:
            planning_markdown += f"#### `{fcr.filename}`\n{blockquote(fcr.instructions)}\n"
    return planning_markdown


if __name__ == "__main__":
    snippet = Snippet(content="test", start=-10, end=10, file_path="test.py", score=1.0)
    print(snippet)
    # bp()
