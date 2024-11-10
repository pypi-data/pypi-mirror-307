from datetime import datetime, timedelta, timezone
from github import Github
from loguru import logger
from tqdm import tqdm
from sweepai.config.server import GITHUB_API_BASE_URL
from sweepai.core.github_utils import github_integration


def get_merged_pr_urls(username: str, token: str | None = None, repos: list[str] | None = None) -> list[str]:
    github_client = github_integration.get_user_installation(username).get_github_for_installation() if not token else Github(token, base_url=GITHUB_API_BASE_URL)
    github_client.per_page = 100
    user = github_client.get_user(username)

    start_date = datetime.now(timezone.utc) - timedelta(days=90)

    logger.info(f"Fetching repos for {username}...")
    github_repos = []
    for repo in tqdm(user.get_repos(type="all", sort="pushed", direction="desc"), desc="Fetching repos"):
        if max(repo.pushed_at, repo.updated_at, repo.created_at) < start_date:
            break
        github_repos.append(repo)

    visited_repos = set([repo.full_name for repo in github_repos])

    events = list(tqdm(user.get_events(), desc="Fetching events"))
    for event in events:
        repo_name = event.raw_data["repo"]["name"]
        if event.created_at < start_date:
            break
        if repo_name not in visited_repos:
            github_repos.append(github_client.get_repo(repo_name))
            visited_repos.add(repo_name)
    
    for repo_name in repos:
        if repo_name and repo_name not in visited_repos:
            github_repos.append(github_client.get_repo(repo_name))
            visited_repos.add(repo_name)

    github_repos.sort(key=lambda x: max(x.pushed_at, x.updated_at, x.created_at), reverse=True)
    logger.info(f"Found {len(github_repos)} repos for {username}...")

    prs = []
    for i, repo in enumerate(github_repos):
        if max(repo.pushed_at, repo.updated_at, repo.created_at) < start_date:
            break
        logger.info(f"Fetching PRs for {repo.name} by {username}...")
        for pr in tqdm(repo.get_pulls(state="closed", sort="updated", direction="desc"), desc=f"Fetching PRs for {repo.name} ({i}/{len(github_repos)})"):
            if (pr.updated_at or pr.created_at) < start_date:
                break
            if pr.user.login == username and pr.merged_at: # can check commits as well but it's super slow
                prs.append(pr)
    urls = [pr.html_url for pr in prs]
    return urls
