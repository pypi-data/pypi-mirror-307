import os

import psutil
from loguru import logger

from sweepai.backend.api_utils import get_cached_installation_id
from sweepai.core.github_utils import REPO_CACHE_BASE_DIR, ClonedRepo
from sweepai.search.agent.entity_search import EntitiesIndex
from sweepai.search.agent.summarize_directory import recursively_summarize_directory
from sweepai.search.query.ticket_utils import prep_snippets


def on_push(repo_full_name: str, tracking_id: str | None = None):
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        logger.info(f"CPU utilization: {cpu_percent}%")
        memory_info = psutil.virtual_memory()
        logger.info(f"Memory utilization: {memory_info.percent}%")
        if cpu_percent >= 50 or memory_info.percent >= 50:
            logger.info(
                f"Skipping update for {repo_full_name} due to high CPU or memory utilization: {cpu_percent}%/{memory_info.percent}%"
            )
            return
        logger.info(f"Updating cloned_repo for {repo_full_name}")
        org_name, repo = repo_full_name.split("/")
        previously_existing_repo_dirs = os.listdir(os.path.join(REPO_CACHE_BASE_DIR, repo_full_name))
        cloned_repo = ClonedRepo(
            repo_full_name, installation_id=get_cached_installation_id(org_name)
        )  # should have latest repo_dir
        is_cloned_repo_dir_the_latest_one = cloned_repo.repo_dir in previously_existing_repo_dirs
        if not is_cloned_repo_dir_the_latest_one:
            prep_snippets(
                cloned_repo=cloned_repo,
                query="DUMMY QUERY",
                skip_reranking=True,
            )
            _, _ = recursively_summarize_directory(cloned_repo, update_summaries=True)
            EntitiesIndex.from_dir(
                cloned_repo.repo_dir,
                key=f"{repo_full_name}:{cloned_repo.branch}",
                no_cache=True,
            )
    except Exception as e:
        logger.error(f"Error updating repo {repo_full_name}: {str(e)}")
