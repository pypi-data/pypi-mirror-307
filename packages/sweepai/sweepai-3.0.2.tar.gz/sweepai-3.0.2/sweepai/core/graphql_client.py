from __future__ import annotations

import requests

from pydantic import BaseModel

from sweepai.config.server import GITHUB_GRAPHQL_BASE_URL
from sweepai.core.github_utils import github_integration, get_token

def generate_error_message(errors: list[dict]) -> str:
    error_message = ""
    for error in errors:
        error_message += error.pop("message") + f", details: {error}\n"
    return error_message

class GitHubGraphQLError(Exception):
    message: str

class GitHubGraphQLClient(BaseModel):
    token: str

    @classmethod
    def from_username(cls, username: str) -> GitHubGraphQLClient:
        installation = github_integration.get_user_installation(username=username)
        token = get_token(installation.id)
        return cls(token=token)

    def query(self, query: str, variables: dict) -> dict:
        response = requests.post(
            GITHUB_GRAPHQL_BASE_URL,
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        response.raise_for_status()
        data = response.json()
        if errors := data.get("errors"):
            raise GitHubGraphQLError(generate_error_message(errors))
        return data
