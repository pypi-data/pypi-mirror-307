import base64
import os
from typing import Literal

from dotenv import load_dotenv
from loguru import logger

logger.print = logger.info

load_dotenv(dotenv_path=".env", override=bool(os.environ.get("ENVIRONMENT")), verbose=True)

# TODO: re-order the constants

os.environ["GITHUB_APP_PEM"] = os.environ.get("GITHUB_APP_PEM") or base64.b64decode(
    os.environ.get("GITHUB_APP_PEM_BASE64", "")
).decode("utf-8")

if os.environ["GITHUB_APP_PEM"]:
    os.environ["GITHUB_APP_ID"] = (
        (os.environ.get("GITHUB_APP_ID") or os.environ.get("APP_ID")).replace("\\n", "\n").strip('"')
    )

TEST_BOT_NAME = "sweep-nightly[bot]"
ENV: Literal["dev", "prod"] = os.environ.get("ENV", "prod")  # dev or prod
DEV: bool = ENV.lower() == "dev"
PROD: bool = ENV.lower() == "prod"
CLI: bool = os.environ.get("CLI", "false").lower() == "true"

BOT_TOKEN_NAME = "bot-token"

SWEEP_HEALTH_URL = os.environ.get("SWEEP_HEALTH_URL")

# For frontend
GITHUB_ID = os.environ.get("GITHUB_ID")
GITHUB_SECRET = os.environ.get("GITHUB_SECRET")

GITHUB_APP_ID = os.environ.get("GITHUB_APP_ID", os.environ.get("APP_ID"))
GITHUB_BOT_USERNAME = os.environ.get("GITHUB_BOT_USERNAME")

GITHUB_LABEL_NAME = os.environ.get("GITHUB_LABEL_NAME", "sweep")
GITHUB_LABEL_COLOR = os.environ.get("GITHUB_LABEL_COLOR", "9400D3")
GITHUB_LABEL_DESCRIPTION = os.environ.get("GITHUB_LABEL_DESCRIPTION", "Sweep your software chores")
GITHUB_APP_PEM = os.environ.get("GITHUB_APP_PEM")
GITHUB_APP_PEM = GITHUB_APP_PEM or os.environ.get("PRIVATE_KEY")
if GITHUB_APP_PEM is not None:
    GITHUB_APP_PEM = GITHUB_APP_PEM.strip(' \n"')  # Remove whitespace and quotes
    GITHUB_APP_PEM = GITHUB_APP_PEM.replace("\\n", "\n")

GITHUB_CONFIG_BRANCH = os.environ.get("GITHUB_CONFIG_BRANCH", "sweep/add-sweep-config")
GITHUB_DEFAULT_CONFIG = os.environ.get(
    "GITHUB_DEFAULT_CONFIG",
    """# Sweep AI turns bugs & feature requests into code changes (https://sweep.dev)
# For details on our config file, check out our docs at https://docs.sweep.dev/usage/config

# This setting contains a list of rules that Sweep will check for. If any of these rules are broken in a new commit, Sweep will create an pull request to fix the broken rule.
rules:
{additional_rules}

# This is the branch that Sweep will develop from and make pull requests to. Most people use 'main' or 'master' but some users also use 'dev' or 'staging'.
branch: 'main'

# By default Sweep will read the logs and outputs from your existing Github Actions. To disable this, set this to false.
gha_enabled: True

# This is the description of your project. It will be used by sweep when creating PRs. You can tell Sweep what's unique about your project, what frameworks you use, or anything else you want.
#
# Example:
#
# description: sweepai/sweep is a python project. The main api endpoints are in sweepai/api.py. Write code that adheres to PEP8.
description: ''

# This sets whether to create pull requests as drafts. If this is set to True, then all pull requests will be created as drafts and GitHub Actions will not be triggered.
draft: False

# This is a list of directories that Sweep will not be able to edit.
blocked_dirs: []
""",
)


ORG_ID = os.environ.get("ORG_ID", None)
POSTHOG_API_KEY = os.environ.get("POSTHOG_API_KEY", "phc_CnzwIB0W548wN4wEGeRuxXqidOlEUH2AcyV2sKTku8n")

if POSTHOG_API_KEY.lower() == "none":
    POSTHOG_API_KEY = None

WHITELISTED_REPOS = os.environ.get("WHITELISTED_REPOS", "").split(",")
BLACKLISTED_USERS = os.environ.get("BLACKLISTED_USERS", "").split(",")

# Default OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)  # this may be none, and it will use azure

OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", "anthropic")
assert OPENAI_API_TYPE in ["anthropic", "azure", "openai"], "Invalid OPENAI_API_TYPE"

AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", None)
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", None)
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", None)

AZURE_API_KEY = os.environ.get("AZURE_API_KEY", None)
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", None)
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION", None)
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", None)

OPENAI_EMBEDDINGS_API_TYPE = os.environ.get("OPENAI_EMBEDDINGS_API_TYPE", "openai")
OPENAI_EMBEDDINGS_AZURE_ENDPOINT = os.environ.get("OPENAI_EMBEDDINGS_AZURE_ENDPOINT", None)
OPENAI_EMBEDDINGS_AZURE_DEPLOYMENT = os.environ.get("OPENAI_EMBEDDINGS_AZURE_DEPLOYMENT", None)
OPENAI_EMBEDDINGS_AZURE_API_VERSION = os.environ.get("OPENAI_EMBEDDINGS_AZURE_API_VERSION", None)

OPENAI_API_ENGINE_GPT35 = os.environ.get("OPENAI_API_ENGINE_GPT35", None)
OPENAI_API_ENGINE_GPT4 = os.environ.get("OPENAI_API_ENGINE_GPT4", None)
MULTI_REGION_CONFIG = os.environ.get("MULTI_REGION_CONFIG", None)
if isinstance(MULTI_REGION_CONFIG, str):
    MULTI_REGION_CONFIG = MULTI_REGION_CONFIG.strip("'").replace("\\n", "\n")
    MULTI_REGION_CONFIG = [item.split(",") for item in MULTI_REGION_CONFIG.split("\n")]

DEFAULT_GPT4_MODEL = os.environ.get("DEFAULT_GPT4_MODEL", "gpt-4o")  # this may break in different envs

FILE_CACHE_DISABLED = os.environ.get("FILE_CACHE_DISABLED", "true").lower() == "true"
GITHUB_BASE_URL = os.environ.get("GITHUB_BASE_URL", "github.com")
GITHUB_ENTERPRISE = GITHUB_BASE_URL != "github.com"
GITHUB_API_BASE_URL = f"https://{GITHUB_BASE_URL}/api/v3" if GITHUB_ENTERPRISE else "https://api.github.com"
GITHUB_GRAPHQL_BASE_URL = f"https://{GITHUB_BASE_URL}/api/graphql" if GITHUB_ENTERPRISE else "https://api.github.com/graphql"

GITHUB_APP_BASE_URL = f"https://{GITHUB_BASE_URL}/github-apps/" if GITHUB_ENTERPRISE else "https://github.com/apps/"
DEFAULT_INSTALL_URL = GITHUB_APP_BASE_URL + (GITHUB_BOT_USERNAME or "").removesuffix("[bot]") + "/installations/select_target"
INSTALL_URL = os.environ.get("INSTALL_URL", DEFAULT_INSTALL_URL)

FRONTEND_URL = (
    os.environ.get("FRONTEND_URL", "")
    or os.environ.get("AUTH_URL", "")
    or os.environ.get("NEXT_AUTH_URL", "")
    or "http://localhost:3000"
).strip("/")

DISABLED_REPOS = os.environ.get("DISABLED_REPOS", "").split(",")

SWEEP_ISSUE_ALLOWLIST: list[str] = os.environ.get("SWEEP_ISSUE_ALLOWLIST", "*").split(",")
FIX_CI_ALLOWLIST: list[str] = os.environ.get("FIX_CI_ALLOWLIST", "*").split(",")

INSTALLATION_ID = os.environ.get("INSTALLATION_ID", None)

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
AWS_ANTHROPIC_BASE_URL = os.environ.get("AWS_ANTHROPIC_BASE_URL")
AWS_ANTHROPIC_AVAILABLE = AWS_ACCESS_KEY and AWS_SECRET_KEY and (AWS_REGION or AWS_ANTHROPIC_BASE_URL)

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", None)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", None)

COHERE_API_KEY = os.environ.get("COHERE_API_KEY", None)

VOYAGE_API_KEY = os.environ.get("VOYAGE_API_KEY", None)

VOYAGE_API_AWS_ACCESS_KEY = os.environ.get("VOYAGE_API_AWS_ACCESS_KEY_ID")
VOYAGE_API_AWS_SECRET_KEY = os.environ.get("VOYAGE_API_AWS_SECRET_KEY")
VOYAGE_API_AWS_REGION = os.environ.get("VOYAGE_API_AWS_REGION")
VOYAGE_API_AWS_ENDPOINT_NAME = os.environ.get("VOYAGE_API_AWS_ENDPOINT_NAME", "voyage-code-2")

VOYAGE_API_USE_AWS = VOYAGE_API_AWS_ACCESS_KEY and VOYAGE_API_AWS_SECRET_KEY and VOYAGE_API_AWS_REGION

# TODO: we need to make this dynamic + backoff
BATCH_SIZE = int(
    os.environ.get(
        "BATCH_SIZE", 64 if VOYAGE_API_KEY else 256
    )  # Voyage only allows 128 items per batch and 120000 tokens per batch
)

JIRA_USER_NAME = os.environ.get("JIRA_USER_NAME", None)
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", None)
JIRA_URL = os.environ.get("JIRA_URL", None)

SLACK_API_KEY = os.environ.get("SLACK_API_KEY", None)

LICENSE_KEY = os.environ.get("LICENSE_KEY", None)
NO_LICENSE = os.environ.get("NO_LICENSE", "false").lower() == "true"
ALTERNATE_AWS = os.environ.get("ALTERNATE_AWS", "none").lower() == "true"

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", None)

SENTRY_URL = os.environ.get("SENTRY_URL", None)

CACHE_DIRECTORY = os.environ.get("CACHE_DIRECTORY", "/mnt/caches")

DOCUMENTATION_URL = os.environ.get("DOCUMENTATION_URL", "https://docs.sweep.dev")

assert OPENAI_API_KEY or AZURE_API_KEY or AZURE_OPENAI_API_KEY or CLI, "OPENAI_API_KEY is required."

CIRCLE_CI_PAT = os.environ.get(
    "CIRCLE_CI_PAT", None
)  # if this is present, we will poll from and get logs from circleci
JENKINS_AUTH = os.environ.get("JENKINS_AUTH", None)

if JENKINS_AUTH:
    JENKINS_AUTH = [tuple(auth.split(":")) for auth in JENKINS_AUTH.split(",") if auth]
    assert all(
        len(auth) == 2 for auth in JENKINS_AUTH
    ), "JENKINS_AUTH must be a comma-separated list of username:api_key pairs"

WHITELISTED_USERS = [user for user in os.environ.get("WHITELISTED_USERS", "").split(",") if user]
assert isinstance(WHITELISTED_USERS, list), "WHITELISTED_USERS must be a list"

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

PREWARM_REPOS = [
    repo.strip() for repo in os.environ.get("PREWARM_REPOS", "").split(",") if repo.strip()
]  # format: org/repo:branch,org/repo2:branch2

CURL_CA_BUNDLE = os.environ.get("CURL_CA_BUNDLE")
AUTHORIZED_USERNAMES = os.environ.get("AUTHORIZED_USERNAMES", "kevinlu1248,wwzeng1,sweep-support").split(",")
DOCKER_BUILDKIT = os.environ.get("DOCKER_BUILDKIT", "1")
