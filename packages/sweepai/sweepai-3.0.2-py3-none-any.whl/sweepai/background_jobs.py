import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from tqdm import tqdm

from sweepai.core.github_utils import REPO_CACHE_BASE_DIR
from sweepai.utils.commit_metrics import get_commit_metrics
from sweepai.web.sync_clock import sync_time

scheduler = BackgroundScheduler()


def run_commit_metrics_computation():
    logger.info("Running commit metrics computation")
    access_token = os.environ.get("GITHUB_PAT")
    _ = get_commit_metrics(access_token, ignore_cache=True)
    # will be cached


def get_repo_commit_hash(repo_dir: str) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_dir, text=True).strip()


def delete_repo_in_background(repo_dir: str):
    subprocess.Popen(
        ["bash", "-c", f"rm -rf {repo_dir} && echo 'Deleted repo {repo_dir}'"],
        start_new_session=True,
    )


def delete_old_repos():
    for base_repo_dir in tqdm(Path(REPO_CACHE_BASE_DIR).rglob("**/base")):
        logger.info(f"Checking {base_repo_dir} for old repos")
        base_dir = base_repo_dir.parent
        directories_to_remove = []
        for git_dir in base_dir.iterdir():
            if git_dir.name == "base" or len(git_dir.name) != 40 or git_dir.is_file():
                continue
            last_read_time = datetime.fromtimestamp(git_dir.stat().st_atime)
            directories_to_remove.append((git_dir, last_read_time))
        directories_to_remove.sort(key=lambda x: x[1])
        if directories_to_remove:
            directories_to_remove.pop()
        logger.info(f"Deleting {len(directories_to_remove)} old repos")
        for directory, last_read_time in directories_to_remove:
            if last_read_time < datetime.now() - timedelta(days=1):
                logger.info(f"Deleting {directory} (last read: {last_read_time})...")
                delete_repo_in_background(str(directory))


scheduler.add_job(
    run_commit_metrics_computation,
    "interval",
    seconds=60 * 60 * 12,  # 12 hours
    max_instances=1,
    next_run_time=datetime.now() + timedelta(minutes=30),
)

scheduler.add_job(sync_time, "interval", seconds=60 * 60, max_instances=1)  # once an hour
scheduler.add_job(delete_old_repos, "cron", hour=1, minute=0, max_instances=1)
