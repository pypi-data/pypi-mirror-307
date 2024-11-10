from typing import Literal
from pydantic import BaseModel
import requests

from sweepai.config.server import DEV
from sweepai.dataclasses.code_suggestions import CodeSuggestion


class SyncManager(BaseModel):
    message_id: str
    github_token: str
    host: str = "http://localhost:8080" if DEV else "https://backend.app.sweep.dev"

    def _request(self, method: Literal["GET", "POST"], path: str, json: dict | None = None):
        response = requests.request(method, f"{self.host}/backend/{path}", json=json, headers={"Authorization": f"Bearer {self.github_token}"})
        response.raise_for_status()
        return response.json()

    def _fetch_changes(self):
        raw_changes = self._request("GET", f"messages/{self.message_id}/changes")
        return [CodeSuggestion.from_camel_case(change) for change in raw_changes]
    
    def _apply_changes(self, changes: list[CodeSuggestion]):
        for change in changes:
            with open(change.file_path, "r") as f:
                assert change.original_code == f.read()
            with open(change.file_path, "w") as f:
                f.write(change.new_code)

    def pull_changes(self):
        changes = self._fetch_changes()
        self._apply_changes(changes)
    
    # def write_changes(self, changes: list[dict]):
    #     self._request("POST", f"messages/{self.message_id}/changes", json={"applied_changes": changes})
