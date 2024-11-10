"""
This module is responsible for handling the check suite event, called from sweepai/api.py
"""

import base64
import fnmatch
import os
import re
import shlex
import subprocess
import time
import zipfile
from contextlib import contextmanager
from dataclasses import dataclass, field
from time import sleep
from typing import Iterator

import psutil
import requests
from github.CommitStatus import CommitStatus
from github.Repository import Repository
from loguru import logger

from sweepai.config.client import get_config_key_value
from sweepai.config.server import CIRCLE_CI_PAT, DOCKER_BUILDKIT, ENV
from sweepai.core.github_utils import ClonedRepo
from sweepai.dataclasses.check_status import CheckStatus
from sweepai.dataclasses.dockerfile_config import (
    DockerfileConfig,
    load_dockerfile_configs_from_path,
)
from sweepai.utils.streamable_functions import streamable
from sweepai.utils.timer import Timer

MAX_LINES = 500
LINES_TO_KEEP = 100
CIRCLECI_SLEEP_DURATION_SECONDS = 15

DOCKERFILE_CONFIG_LOCATION = os.path.join(os.getcwd(), "dockerfiles")

log_message = """GitHub actions yielded the following error.

{error_logs}

Fix the code changed by the PR, don't modify the existing tests."""


def get_dirs(zipfile: zipfile.ZipFile):
    return [file for file in zipfile.namelist() if file.endswith("/") and "/" in file]


def get_files_in_dir(zipfile: zipfile.ZipFile, dir: str):
    return [file for file in zipfile.namelist() if file.startswith(dir) and not file.endswith("/")]


def remove_ansi_tags(logs: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", logs, flags=re.MULTILINE)


gha_prompt = """\
The below command yielded the following errors:
<command>
{command_line}
</command>
<errors>
{error_content}
</errors>
Here are the logs:
<logs>
{cleaned_logs_str}
</logs>"""


@contextmanager
def change_dir(destination):
    prev_dir = os.getcwd()
    os.chdir(destination)
    try:
        yield
    finally:
        os.chdir(prev_dir)


@contextmanager
def changes_applied(cloned_repo: ClonedRepo, file_changes: dict):
    prev_files = {}
    try:
        # Save the changes and apply them
        for file_path, file_contents in file_changes.items():
            try:
                with open(os.path.join(cloned_repo.repo_dir, file_path), "r+") as file:
                    prev_files[file_path] = file.read()
                    file.seek(0)
                    file.write(file_contents)
                    file.truncate()
            except FileNotFoundError:
                logger.warning(f"File {file_path} not found in repo {cloned_repo.repo_dir}")
        yield
    finally:
        # Restore the original files
        for file_path, file_contents in prev_files.items():
            with open(os.path.join(cloned_repo.repo_dir, file_path), "w") as file:
                file.write(file_contents)


@dataclass
class DockerContainer:
    container_id: str
    file_changes: dict = field(default_factory=dict)

    def exec(self, command: str):
        return subprocess.run(
            f"docker exec {self.container_id} sh -c {shlex.quote(command)}",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )

    def exec_stream(self, command: str):
        return subprocess.Popen(
            f"docker exec {self.container_id} sh -c {shlex.quote(command)}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def pull_file_changes(self):
        for file_path in self.file_changes:
            results = self.exec(f"cat {shlex.quote(file_path)}")
            self.file_changes[file_path] = results.stdout


@contextmanager
def running_docker_container(
    image_name: str,
    container_name: str,
    file_changes: dict,
    env_path: str = "",
) -> Iterator[DockerContainer]:
    # Helper function to start up container, apply changes, move to cwd, and remove container after it exits
    if env_path:
        run_command = f"docker run --env-file {env_path} --name {container_name} -d {image_name} sleep infinity"
    else:
        run_command = f"docker run --name {container_name} -d {image_name} sleep infinity"

    results = subprocess.run(run_command, shell=True, check=True, capture_output=True, text=True)
    container_id = results.stdout.strip()

    container = DockerContainer(container_id, file_changes)

    make_changes_command = ""
    for file_path, file_contents in file_changes.items():
        dir_path = os.path.dirname(file_path)
        if dir_path:
            # Create the directory if it doesn't exist
            make_changes_command += f"mkdir -p {shlex.quote(dir_path)} && "
        # Write the file contents
        encoded_contents = base64.b64encode(file_contents.encode()).decode()
        # Base64 encoding prevents \n from being interpreted as separate lines
        command = f"echo {shlex.quote(encoded_contents)} | base64 -d > {shlex.quote(file_path)}"
        make_changes_command += f"{command} && "
    make_changes_command = make_changes_command.removesuffix(" && ")

    container.exec(make_changes_command)

    try:
        yield container
    finally:
        container.pull_file_changes()
        subprocess.run(
            f"docker kill {container_id} && docker rm {container_id}",
            shell=True,
            check=True,
        )


@streamable
def get_failing_docker_logs(
    cloned_repo: ClonedRepo,
    file_changes: dict,
):
    """
    Input: ClonedRepo object
    Output:
    - logs, a string containing the logs of the failing docker container
    - image_name, a string containing the name of the docker image (for later cleanup)
    """
    # image name should be an input arg and cleaned up at the end
    dockerfile_config_path = os.path.join(DOCKERFILE_CONFIG_LOCATION, cloned_repo.repo_full_name, "config.json")
    if not os.path.exists(dockerfile_config_path):
        logger.warning(f"Docker not configured for {cloned_repo.repo_full_name}")
        return "", []
    dockerfile_configs = load_dockerfile_configs_from_path(dockerfile_config_path)

    if not dockerfile_configs:
        # this method should not be called if the dockerfile config is not present
        return "", ""

    # Get CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Get memory usage
    memory = psutil.virtual_memory()
    memory_percent = memory.percent

    # Get disk usage
    disk = psutil.disk_usage("/")
    disk_percent = disk.percent

    # Log system resource usage
    logger.info(f"System resource usage: CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")

    # Get the number of running Docker processes
    docker_processes = subprocess.check_output(["docker", "ps", "-q"], text=True).splitlines()
    num_docker_processes = len(docker_processes)

    # Check if resource usage is too high
    if ENV == "prod" and (cpu_percent > 50 or memory_percent > 50 or disk_percent > 80 or num_docker_processes > 3):
        logger.warning("System resources are critically low. Docker build may fail or perform poorly.")
        raise Exception("System resources are critically low. Try again later.")

    @streamable
    def run_dockerfile_config(
        dockerfile_config: DockerfileConfig,
        cloned_repo: ClonedRepo,
        file_changes: dict,
    ):
        image_name = dockerfile_config.image_name + "-" + os.path.basename(cloned_repo.repo_dir)[:8]
        container_name = dockerfile_config.container_name + "-" + str(hash(cloned_repo.repo_dir))[-8:]
        dockerfile_path = dockerfile_config.dockerfile_path
        env_path = os.path.join(
            os.path.join(
                os.getcwd(),
                DOCKERFILE_CONFIG_LOCATION,
                cloned_repo.repo_full_name,
                ".env",
            )
        )
        _env_exists = os.path.exists(env_path)
        dockerfile_path = os.path.join(
            os.getcwd(),
            DOCKERFILE_CONFIG_LOCATION,
            cloned_repo.repo_full_name,
            dockerfile_path,
        )
        logs = ""

        status: CheckStatus = {
            "message": "",
            "stdout": "",
            "succeeded": None,
            "status": "running",
            "llm_message": "",
            "container_name": container_name,
            "start_time": -1,
            "end_time": -1,
        }
        with Timer():
            try:
                # TODO: add !.git to dockerignore
                with change_dir(cloned_repo.repo_dir):
                    # Build the Docker image
                    if DOCKER_BUILDKIT == "0":
                        build_command = f"DOCKER_BUILDKIT={DOCKER_BUILDKIT} docker build -t {image_name} -f {dockerfile_path} --build-arg CODE_PATH=. ."
                    else:
                        build_command = f"DOCKER_BUILDKIT={DOCKER_BUILDKIT} docker build --progress=plain -t {image_name} -f {dockerfile_path} --build-arg CODE_PATH=. ."
                    status["message"] = "Building Docker image..."
                    yield status, file_changes
                    status["start_time"] = time.time()
                    with Timer():
                        # Use Popen to stream output
                        stdout = ""
                        with subprocess.Popen(
                            build_command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                        ) as proc:
                            for line in proc.stdout:
                                print(line, end="", flush=True)
                                stdout += line
                                status["stdout"] = stdout
                                yield status, file_changes
                    logger.info(f"Built Docker image {image_name}")
                    # Check if the build process failed
                    if proc.returncode != 0:
                        status["message"] = "Docker build failed"
                        status["status"] = "failure"
                        status["succeeded"] = False
                        yield status, file_changes
                        return (
                            f"Docker build failed with exit code {proc.returncode}",
                            image_name,
                        )

                    env_path = ""

                    with running_docker_container(image_name, container_name, file_changes, env_path) as container:
                        # Find and dedup all file paths relative to the working directory
                        if dockerfile_config.working_dir:
                            file_paths = sorted(
                                [
                                    key.replace(dockerfile_config.working_dir.rstrip("/"), ".")
                                    for key in file_changes.keys()
                                    if key.startswith(dockerfile_config.working_dir)
                                ]
                            )
                        else:
                            file_paths = sorted(file_changes.keys())
                        file_paths_string = " ".join(file_paths)
                        file_dirs = list(set([os.path.dirname(file_path) for file_path in file_paths]))
                        file_dirs_string = " ".join(file_dirs)
                        base_command = dockerfile_config.command.replace("$FILE_PATHS", file_paths_string).replace(
                            "$FILE_DIRS", file_dirs_string
                        )

                        if dockerfile_config.working_dir:
                            run_command = f"cd {shlex.quote(dockerfile_config.working_dir)} && {base_command}"
                        else:
                            run_command = base_command

                        status["message"] = "Running Docker image..."
                        yield status, file_changes

                        logger.info(f"Running Docker image {image_name}...")
                        with Timer():
                            # Use Popen to stream output
                            stdout = f"$ ({dockerfile_config.working_dir or '~'}) {base_command}\n\n"
                            status["stdout"] = stdout
                            yield status, file_changes
                            with container.exec_stream(run_command) as proc:
                                for line in proc.stdout:
                                    print(line, end="", flush=True)
                                    stdout += line
                                    status["stdout"] = stdout
                                    yield status, file_changes
                        status["end_time"] = time.time()
                        status["message"] = f"Checks passed" if proc.returncode == 0 else f"Checks failed"
                        status["status"] = "success" if proc.returncode == 0 else "failure"
                        status["succeeded"] = proc.returncode == 0
                        yield status, file_changes

                    if proc.returncode == 0:
                        file_changes = container.file_changes

                    return "", image_name
            except subprocess.CalledProcessError as e:
                # TODO: handle this case
                logs = e.stdout + e.stderr
                logger.error(f"Error running Docker image {image_name}: {logs}")
            gha_formatted_prompt = gha_prompt.format(
                command_line=dockerfile_config.command,
                error_content=logs,
                cleaned_logs_str="",
            )
            status["message"] = "Checks failed"
            status["succeeded"] = False
            status["stdout"] = logs
            status["llm_message"] = gha_formatted_prompt
            yield status, file_changes
            return gha_formatted_prompt, image_name

    # run dockerfile configs in parallel
    docker_logs = ""
    image_names = []
    statuses = []
    new_dockerfile_configs = []
    for dockerfile_config in dockerfile_configs:
        did_match = False
        for file_glob in dockerfile_config.match_files:
            if any(fnmatch.fnmatch(file_path, file_glob) for file_path in file_changes.keys()):
                did_match = True
                break
        if did_match:
            new_dockerfile_configs.append(dockerfile_config)
    dockerfile_configs = new_dockerfile_configs

    for dockerfile_config in dockerfile_configs:
        statuses.append(
            {
                "message": "Queued",
                "stdout": "",
                "succeeded": None,
                "status": "pending",
                "llm_message": "",
                "container_name": dockerfile_config.container_name + "-" + str(hash(cloned_repo.repo_dir))[-8:],
            }
        )
    for i, dockerfile_config in enumerate(dockerfile_configs):
        for status, file_changes in run_dockerfile_config.stream(dockerfile_config, cloned_repo, file_changes):
            statuses[i] = status
            yield statuses, file_changes
        if not status["succeeded"]:
            statuses[i + 1 :] = [
                {**status, "status": "cancelled", "message": "Check cancelled"} for status in statuses[i + 1 :]
            ]
            yield statuses, file_changes
            break  # stop at the first failing docker container
    # TODO: delete all images > 2 hours old
    return docker_logs, image_names


def delete_docker_images(docker_image_names: str):
    for image_name in docker_image_names:
        delete_command = f"docker rmi {image_name}"
        try:
            subprocess.run(delete_command, shell=True, check=True)
            logger.info(f"Deleted Docker image: {image_name}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Error deleting Docker image: {image_name}")
            logger.warning(f"Error message: {str(e)}")


def clean_gh_logs(logs_str: str):
    """
    TODO: this can be made without the XML and truncation
    """
    # Extraction process could be better
    log_list = logs_str.split("\n")
    truncated_logs = [log[log.find(" ") + 1 :] for log in log_list]
    logs_str = "\n".join(truncated_logs)
    # extract the group and delete everything between group and endgroup
    gha_pattern = r"##\[group\](.*?)##\[endgroup\](.*?)(##\[error\].*)"
    match = re.search(gha_pattern, logs_str, re.DOTALL)
    if not match:
        return "\n".join(logs_str.split("\n")[:MAX_LINES])
    command_line = match.group(1).strip()
    log_content = match.group(2).strip()
    error_line = match.group(3).strip()  # can be super long
    return clean_cicd_logs(
        command=command_line,
        error=error_line,
        logs=log_content,
    )


def clean_cicd_logs(command: str, error: str, logs: str):
    patterns = [
        # for docker
        "Already exists",
        "Pulling fs layer",
        "Waiting",
        "Download complete",
        "Verifying Checksum",
        "Pull complete",
        # For github
        "remote: Counting objects",
        "remote: Compressing objects:",
        "Receiving objects:",
        "Resolving deltas:",
        "[command]/usr/bin/git ",
        "Download action repository",
        # For python
        "Collecting",
        "Downloading",
        "Installing",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        # For prettier
        "npm WARN EBADENGINE ",
        "npm WARN deprecated ",
        "prettier/prettier",
    ]
    cleaned_logs = [
        log.strip() for log in logs.split("\n") if not any(log.strip().startswith(pattern) for pattern in patterns)
    ]
    if len(cleaned_logs) > MAX_LINES:
        # return the first LINES_TO_KEEP and the last LINES_TO_KEEP
        cleaned_logs = cleaned_logs[:LINES_TO_KEEP] + ["..."] + cleaned_logs[-LINES_TO_KEEP:]
    cleaned_logs_str = "\n".join(cleaned_logs)
    error_content = ""
    if len(error) < 200000:
        error_content = f"""<errors>
{error}
</errors>"""
    cleaned_response = gha_prompt.format(
        command_line=command,
        error_content=error_content,
        cleaned_logs_str=cleaned_logs_str,
    )
    return cleaned_response


def get_circleci_job_details(job_number, project_slug, vcs_type="github"):
    # project_slug is the repo full name
    headers = {"Circle-Token": CIRCLE_CI_PAT}
    url = f"https://circleci.com/api/v1.1/project/{vcs_type}/{project_slug}/{job_number}"
    response = requests.get(url, headers=headers)
    return response.json()


# take a commit and return all failing logs as a list
def get_failing_circleci_log_from_url(circleci_run_url: str, repo_full_name: str):
    if not CIRCLE_CI_PAT:
        logger.warning("CIRCLE_CI_APIKEY not set")
        return []
    headers = {"Circle-Token": CIRCLE_CI_PAT}
    job_number = circleci_run_url.split("/")[-1]
    circleci_run_details = get_circleci_job_details(job_number, repo_full_name)
    steps = circleci_run_details["steps"]
    failing_steps = []
    failed_commands_and_logs = ""
    for step in steps:
        if step["actions"][0]["exit_code"] != 0:
            failing_steps.append(step)
    for step in failing_steps:
        actions = step["actions"]
        for action in actions:
            if action.get("status") != "failed":
                continue
            if "output_url" in action:
                log_url = action["output_url"]
                log_response = requests.get(log_url, headers=headers)
                log_response = log_response.json()
                # these might return in a different order; watch out
                log_message = log_response[0]["message"] if len(log_response) > 0 else ""
                error_message = log_response[1].get("message", "") if len(log_response) > 1 else ""
                log_message = remove_ansi_tags(log_message)
                error_message = remove_ansi_tags(error_message)
                command = action.get("bash_command", "No command found.")  # seems like this is the only command
                circle_ci_failing_logs = clean_cicd_logs(
                    command=command,
                    error=error_message,
                    logs=log_message,
                )
                if circle_ci_failing_logs:
                    failed_commands_and_logs += circle_ci_failing_logs + "\n"
    return failed_commands_and_logs


def get_failing_circleci_logs(
    repo: Repository,
    current_commit: str,
):
    # get the pygithub commit object
    all_logs = ""
    failing_statuses = []
    total_poll_attempts = 0
    # hacky workaround because circleci can have a setup that takes a long time, and we will report "success" because the setup has finished but the actual CI is still running
    logger.debug("Waiting for 60 seconds before polling for CircleCI status.")
    sleep(60)
    while True:
        commit = repo.get_commit(current_commit)
        status = commit.get_combined_status()
        # https://docs.github.com/en/rest/commits/statuses?apiVersion=2022-11-28#get-the-combined-status-for-a-specific-reference
        all_statuses: list[CommitStatus] = status.statuses
        # if all are success, break
        if all(status.state == "success" for status in all_statuses):
            failing_statuses = []
            logger.debug(f"Exiting polling for CircleCI as all statuses are success. Statuses were: {all_statuses}")
            break
        # if any of the statuses are failure, return those statuses
        failing_statuses = [status for status in all_statuses if status.state == "failure"]
        if failing_statuses:
            logger.debug(f"Exiting polling for CircleCI as some statuses are failing. Statuses were: {all_statuses}")
            break
        # if any of the statuses are pending, sleep and try again
        if any(status.state == "pending" for status in all_statuses):
            if total_poll_attempts * CIRCLECI_SLEEP_DURATION_SECONDS // 60 >= 60:
                logger.debug("Polling for CircleCI has taken too long, giving up.")
                break
            # wait between check attempts
            total_poll_attempts += 1
            logger.debug(f"Polling to see if CircleCI has finished... {total_poll_attempts}.")
            sleep(CIRCLECI_SLEEP_DURATION_SECONDS)
            continue
    # filter out statuses that are not allowed
    # this only executes if allowed_cicd_names is not None
    allowed_cicd_names = get_config_key_value(repo, "allowed_cicd_names")
    if allowed_cicd_names:
        failing_statuses = [
            status
            for status in failing_statuses
            if any(cicd_name in status.context.lower() for cicd_name in allowed_cicd_names)
        ]
    # done polling
    for status_detail in failing_statuses:
        # CircleCI run detected
        if "circleci" in status_detail.context.lower():
            failing_circle_ci_log = get_failing_circleci_log_from_url(
                circleci_run_url=status_detail.target_url, repo_full_name=repo.full_name
            )  # may be empty string
            if failing_circle_ci_log:
                all_logs += failing_circle_ci_log + "\n"
    return all_logs
