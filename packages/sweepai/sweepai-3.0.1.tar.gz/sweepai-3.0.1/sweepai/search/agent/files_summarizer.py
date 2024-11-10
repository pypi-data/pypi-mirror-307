import os
import sys
from typing import Dict, List

import joblib
from diskcache import Cache
from loguru import logger
from tqdm import tqdm

from sweepai.config.client import SweepConfig
from sweepai.config.server import CACHE_DIRECTORY, DEV
from sweepai.core.github_utils import ClonedRepo
from sweepai.core.llm.chat import call_llm
from sweepai.search.agent.summarize_directory import recursively_summarize_directory
from sweepai.search.query.repo_parsing_utils import is_actual_code_file
from sweepai.utils.cache import hash_code
from sweepai.utils.str_utils import extract_xml_tag

file_summary_cache = Cache(f"{CACHE_DIRECTORY}/file_summary_cache")

instructions = "Start by explaining the the file in the context of its directories. Focus on nuances and patterns. Then, explain what types of business logic this file contains. For each code entity, explain its purpose and what it handles. Be concise and optimize for informational density. One paragraph."

system_prompt = "Your job is to summarize the following file. " + instructions

user_prompt = (
    """First, review the parent directory summaries for context:

<directory_summaries>
{DIRECTORY_SUMMARIES}
</directory_summaries>

Now, examine the title and contents of the file:

<file_name>
{FILE_NAME}
</file_name>

<file_contents>
{FILE_CONTENTS}
</file_contents>

Provide your summary within <file_summary> tags.

<file_summary>
[Your concise, one-paragraph summary goes here]
</file_summary>

"""
    + instructions
)


class FilesSummarizer:
    def __init__(self, cloned_repo: ClonedRepo):
        self.cloned_repo = cloned_repo
        logger.info("Summarizing directories...")
        self.directory_summaries, _ = recursively_summarize_directory(self.cloned_repo)
        logger.info("Summarizing files...")
        self.file_summaries = self.generate_file_summaries()

    def get_ancestors(self, relative_path: str) -> List[str]:
        """Given a relative_path, compute all possible ancestors"""
        parts = relative_path.split(os.sep)
        ancestors = []
        for i in range(1, len(parts)):
            ancestor = os.path.join(*parts[:i])
            ancestors.append(ancestor)
        return ancestors

    def get_ancestor_summaries(self, relative_path: str) -> Dict[str, str]:
        """Given a relative_path, construct a Dict with key is ancestor path and value is the summary"""
        ancestor_summaries = {}
        ancestors = self.get_ancestors(relative_path)
        for ancestor in ancestors:
            if ancestor in self.directory_summaries:
                ancestor_summaries[ancestor] = self.directory_summaries[ancestor]
        return ancestor_summaries

    def summarize_file(self, absolute_path: str, relative_path: str, verbose: bool = False) -> str:
        """
        absolute_path: for opening file
        relative_path: for getting ancestor directory summaries
        """
        try:
            with open(absolute_path, "r", encoding="utf-8") as f:
                file_contents = f.read()
        except (UnicodeDecodeError, IOError) as e:
            logger.warning(f"Error reading file {relative_path}: {str(e)}")
            # if the file can't be opened (e.g. it's an image), use the file name as content
            file_contents = os.path.basename(absolute_path)

        if len(file_contents.splitlines()) > 10000:  # Skip large files
            return ""

        file_hash = hash_code(file_contents)

        if (results := file_summary_cache.get(file_hash)) is not None:
            return results

        # TODO: use older file contents in dev
        if DEV:
            try:
                commits = self.cloned_repo.git_repo.git.log(relative_path, n=10, format="%H").splitlines()
                for commit in commits:
                    try:
                        previous_file_contents = self.cloned_repo.git_repo.git.show(f"{commit}:{relative_path}")
                        if (results := file_summary_cache.get(hash_code(previous_file_contents))) is not None:
                            return results
                    except Exception as e:
                        if "exists on disk, but not in" in str(e):
                            # File didn't exist in this commit, skip to the next one
                            continue
                        else:
                            logger.warning(f"Error getting previous file contents for {relative_path}: {str(e)}")
            except Exception as e:
                logger.warning(f"Error getting previous file contents for {relative_path}: {str(e)}")

        ancestor_summaries = self.get_ancestor_summaries(relative_path)

        directory_summaries = ""
        for ancestor, summary in ancestor_summaries.items():
            directory_summaries += f"{ancestor}\n{summary}\n\n"
        directory_summaries = directory_summaries.strip()

        response = call_llm(
            system_prompt,
            user_prompt,
            params={
                "DIRECTORY_SUMMARIES": directory_summaries,
                "FILE_NAME": relative_path,
                "FILE_CONTENTS": file_contents,
            },
            verbose=False,
        )
        summary = extract_xml_tag(response, "file_summary")
        file_summary_cache[file_hash] = summary
        return summary

    def generate_file_summaries(self):
        """Walk through the cloned repo and generate summaries for all code files in parallel"""
        file_summaries = {}
        sweep_config = SweepConfig()
        files_to_summarize = []

        # Collect all files to summarize
        for root, dirs, files in os.walk(self.cloned_repo.repo_dir):
            dirs[:] = [d for d in dirs if d not in sweep_config.exclude_dirs]
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, self.cloned_repo.repo_dir)
                if is_actual_code_file(root, absolute_path, sweep_config):
                    files_to_summarize.append((absolute_path, relative_path))

        def summarize_wrapper(args):
            abs_path, rel_path = args
            try:
                return rel_path, self.summarize_file(abs_path, rel_path)
            except Exception as e:
                logger.error(f"Error summarizing {rel_path}: {str(e)}")
                return rel_path, None

        workers = min(4, len(files_to_summarize)) if DEV else 1
        # WARNING: this is unsafe because it can trigger an ValuError: I/O operation on closed file
        if files_to_summarize:
            results = joblib.Parallel(n_jobs=workers, prefer="threads")(
                joblib.delayed(summarize_wrapper)(args)
                for args in tqdm(files_to_summarize, desc="Summarizing files", file=sys.stderr)
            )

            file_summaries.update({rel_path: summary for rel_path, summary in results if summary is not None})

        return file_summaries


if __name__ == "__main__":
    from sweepai.core.github_utils import github_integration

    REPO = os.environ["REPO"]
    org_name, repo_name = REPO.split("/")
    installation_id = github_integration.get_repo_installation(org_name, repo_name)
    cloned_repo = ClonedRepo(REPO, installation_id=installation_id)
    file_summarizer = FilesSummarizer(cloned_repo=cloned_repo)
    # print(file_summarizer.file_summaries)
