from dataclasses import dataclass


@dataclass
class DirectorySummariesRequest:
    repo_name: str
    directories: list[str]
