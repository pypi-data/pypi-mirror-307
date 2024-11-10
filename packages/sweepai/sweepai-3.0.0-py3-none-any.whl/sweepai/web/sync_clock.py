from datetime import datetime
import subprocess

from loguru import logger
import requests
from sweepai.config.server import DEV, GITHUB_BASE_URL

def get_github_time():
    """Fetch current time from GitHub API"""
    response = requests.get(f"https://{GITHUB_BASE_URL}")
    response.raise_for_status()
    # Parse the date from response headers
    github_time = response.headers['date']
    return datetime.strptime(github_time, '%a, %d %b %Y %H:%M:%S GMT')

def set_system_time(dt: datetime):
    return subprocess.run(f'date -s "{dt.strftime("%Y-%m-%d %H:%M:%S")}"', shell=True, check=True)

def sync_time():
    """Main function to sync system time with GitHub"""
    if DEV:
        return
    current_time = datetime.utcnow()
    github_time = get_github_time()
    logger.info(f"Current time: {current_time}, GitHub time: {github_time}, time diff: {(current_time - github_time).total_seconds()} seconds")
    set_system_time(github_time)

    # Verify that the system time is within 5 seconds of the GitHub time
    current_time = datetime.utcnow()
    new_github_time = get_github_time()
    time_diff = (current_time - new_github_time).total_seconds()
    if abs(time_diff) > 5:
        raise Exception(f"System time differs from GitHub time by {time_diff} seconds")
    else:
        logger.info(f"System time synchronized with GitHub: {github_time}, time diff: {time_diff} seconds")

if __name__ == "__main__":
    sync_time() # needs --cap-add SYS_TIME -v /etc/localtime:/etc/localtime
