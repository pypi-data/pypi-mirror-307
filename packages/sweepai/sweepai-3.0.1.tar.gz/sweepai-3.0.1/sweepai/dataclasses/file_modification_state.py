from __future__ import annotations

from dataclasses import dataclass, field

from sweepai.utils.diff import generate_diff


@dataclass
class FileContents:
    original_contents: str
    new_contents: str

    @property
    def has_changes(self) -> bool:
        return self.original_contents != self.new_contents
    
    def diff(self) -> str:
        return generate_diff(self.original_contents, self.new_contents)
    
    def __repr__(self) -> str:
        return self.diff()


@dataclass
class FileModificationState:
    files: dict[str, FileContents] = field(default_factory=dict)

    def get_original_contents(self, file_path: str) -> str:
        return self.files[file_path].original_contents

    def get_new_contents(self, file_path: str) -> str:
        return self.files[file_path].new_contents

    def add_or_update_file(self, file_path: str, original_contents: str, new_contents: str):
        self.files[file_path] = FileContents(original_contents, new_contents)

    def update_original_contents(self, file_path: str, new_contents: str):
        self.files[file_path].original_contents = new_contents

    def update_new_contents(self, file_path: str, new_contents: str):
        self.files[file_path].new_contents = new_contents

    def file_has_changes(self, file_path: str) -> bool:
        return self.files[file_path].has_changes

    def dict(self) -> dict:
        """
        Dumps this object to a dictionary.
        """
        return {
            "files": {
                file_path: {
                    "original_contents": contents.original_contents,
                    "new_contents": contents.new_contents,
                }
                for file_path, contents in self.files.items()
            }
        }
    
    def to_raw_code_suggestions(self) -> list[dict[str, str]]:
        return [
            {
                "filePath": file_path,
                "originalCode": contents.original_contents,
                "newCode": contents.new_contents,
                "state": "done",
            }
            for file_path, contents in self.files.items()
        ]

    
    def __getitem__(self, file_path: str) -> FileContents:
        return self.files[file_path]
    
    def __len__(self):
        return len(self.files)

    def __contains__(self, file_path: str) -> bool:
        return file_path in self.files
    
    def __iter__(self):
        return iter(self.files)

    @classmethod
    def from_dict(cls, dict: dict) -> FileModificationState:
        # Handles legacy dicts
        file_modification_state = FileModificationState()
        for file_path, file_content in dict.items():
            file_modification_state.add_or_update_file(
                file_path, file_content["original_contents"], file_content["contents"]
            )
        return file_modification_state
    
    def diff(self) -> str:
        return "\n\n".join([f"#### {file_path}\n\n{file_contents.diff()}" for file_path, file_contents in self.files.items()])
    
    def __repr__(self) -> str:
        return self.diff()
