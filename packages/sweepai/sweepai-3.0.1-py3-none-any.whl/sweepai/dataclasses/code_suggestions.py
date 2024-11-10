import uuid
from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class CodeSuggestion:
    file_path: str
    original_code: str
    new_code: str
    file_contents: str = ""
    id: str = field(default_factory=lambda: "pyid-" + str(uuid.uuid4()))

    def to_camel_case(self):
        return {
            "filePath": self.file_path,
            "originalCode": self.original_code,
            "newCode": self.new_code,
        }
    
    @classmethod
    def from_camel_case(cls, data: dict):
        return cls(
            file_path=data["filePath"],
            original_code=data["originalCode"],
            new_code=data["newCode"],
        )


@dataclass
class StatefulCodeSuggestion(CodeSuggestion):
    state: Literal["pending", "processing", "done", "error"] = "pending"
    error: Optional[str] = None

    def to_camel_case(self):
        return {
            **super().to_camel_case(),
            "state": self.state,
        }
    
    @classmethod
    def from_camel_case(cls, data: dict):
        suggestion = super().from_camel_case(data)
        suggestion.state = data["state"]
        return suggestion
