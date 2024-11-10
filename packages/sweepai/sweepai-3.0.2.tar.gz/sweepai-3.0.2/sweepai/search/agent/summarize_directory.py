import os

from anytree import Node, RenderTree
from diskcache import Cache
from loguru import logger
from tqdm import tqdm

from sweepai.config.client import SweepConfig
from sweepai.config.server import CACHE_DIRECTORY
from sweepai.core.entities import SNIPPET_FORMAT, Snippet
from sweepai.core.github_utils import ClonedRepo
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, call_llm
from sweepai.search.query.repo_parsing_utils import is_actual_code_file
from sweepai.utils.str_utils import extract_xml_tag, pack_items_for_prompt
from sweepai.utils.timer import Timer

summary_caches = Cache(f"{CACHE_DIRECTORY}/summary_caches")

FILE_THRESHOLD = 500


def estimate_line_count(filename):
    stat = os.stat(filename)
    # Get file size
    file_size = stat.st_size
    # Read at most 8000 bytes, ~160 lines of python code to estimate average line length.
    # Obvious limitations here but it's a good enough heuristic for now. Overestimates for short lines.
    sample_size = min(file_size, 8000)
    with open(filename, "rb") as f:
        sample = f.read(sample_size)
    # Count newlines in the sample
    sample_newlines = sample.count(b"\n")
    # Estimate average line length
    if sample_newlines == 0:
        return 1  # Assume it's a one-line file if no newlines in sample
    avg_line_length = len(sample) / sample_newlines
    # Estimate total lines
    estimated_lines = int(file_size / avg_line_length)
    return estimated_lines


def count_descendants_files_or_lines_of_code(directory: str, count_lines_of_code: bool = False):
    sweep_config = SweepConfig()
    descendant_count = {}
    dir_file_count = {}

    def is_dir_too_big(file_name: str):
        dir_name = os.path.dirname(file_name)
        file_sections = file_name.split(os.sep)
        # use filter_file here
        for name in (
            ".git",
            "node_modules",
            ".venv",
            "build",
            "venv",
            "patch",
            ".next",
        ):
            if name in file_sections:
                return True
        if dir_name not in dir_file_count:
            dir_file_count[dir_name] = len(os.listdir(dir_name))
        return dir_file_count[dir_name] > FILE_THRESHOLD

    def dfs(current_dir):
        count = 0
        for root, sub_paths, files in os.walk(current_dir):
            if is_dir_too_big(root):
                continue
            for sub_path in sub_paths:
                if is_dir_too_big(os.path.join(root, sub_path)):
                    continue
                count += dfs(os.path.join(root, sub_path))
            if count_lines_of_code:
                for file in files:
                    if is_actual_code_file(root, os.path.join(root, file), sweep_config):
                        # add number of estimated newlines in file
                        count += estimate_line_count(os.path.join(root, file))
            else:
                count += len(files)
        descendant_count[current_dir.removeprefix(directory.rstrip() + "/")] = count
        return count

    print("Counting descendants")
    with Timer():
        dfs(directory)
    print("Done counting descendants")
    for key in (".git", ""):
        if key in descendant_count:
            del descendant_count[key]
    descendant_count["/"] = descendant_count[directory]
    del descendant_count[directory]
    return descendant_count


# include files, and important structural information from the readme
instructions = "Start by explaining the high-level purpose of the directory and its subdirectories. Focus on nuances and patterns. Then, explain what types of business logic this directory contains, with examples from specific files and directories. Only list describe contents that appear in multiple files. Be concise and optimize for informational density. One paragraph."

system_prompt = "Your job is to summarize the following directory from the repository. " + instructions

user_prompt = (
    """Summarize the following directory from the repository.

Repository:
{repo_name}

Directory:
{directory}

<example_files>
{snippets_string}
</example_files>

"""
    + instructions
)


def summarize_directory(
    directory: str,
    snippets: list[Snippet],
    cloned_repo: ClonedRepo,
    directory_summaries: dict[str, str] = {},
):
    key = (
        "summary",
        cloned_repo.repo_full_name,
        "\n".join([snippet.denotation for snippet in snippets]),
    )
    if key in summary_caches:
        return summary_caches[key]
    directory_files = sorted(
        [
            subdir
            for subdir in os.listdir(os.path.join(cloned_repo.repo_dir, directory))
            if os.path.isfile(os.path.join(cloned_repo.repo_dir, directory, subdir))
        ]
    )
    directory_subdirs = sorted(
        [
            subdir
            for subdir in os.listdir(os.path.join(cloned_repo.repo_dir, directory))
            if os.path.isdir(os.path.join(cloned_repo.repo_dir, directory, subdir))
        ]
    )

    snippets_string = "\n\n".join(
        [
            SNIPPET_FORMAT.format(
                denotation=snippet.denotation,
                contents=snippet.expand(50).get_snippet(False, False),
                index=index,
            )
            for index, snippet in enumerate(snippets)
        ]
    )

    other_files_string = ""
    for file in directory_files:
        if file not in [snippet.file_path for snippet in snippets]:
            other_files_string += "- " + file + "\n"
    if other_files_string:
        snippets_string += f"\n\nThe directory also contains the following files:\n\n" + other_files_string

    for subdir, summary in directory_summaries.items():
        if subdir.startswith(directory) and summary:
            snippets_string += f"\n\nHere is a summary of the subdirectory {subdir}:\n\n" + summary

    subdirs_string = ""
    for subdir in directory_subdirs:
        if subdir not in directory_summaries:
            subdirs_string += "- " + subdir + "\n"
    if subdirs_string:
        snippets_string += f"\n\nThe directory also contains the following subdirectories:\n\n" + subdirs_string

    response = call_llm(
        system_prompt,
        user_prompt,
        params={
            "repo_name": cloned_repo.repo_full_name,
            "directory": directory,
            "snippets_string": snippets_string.strip(),
        },
        verbose=False,
    )
    summary_caches[key] = response

    return response


NUM_SNIPPET_EXAMPLES = 10


def get_last_commit_time(cloned_repo: ClonedRepo, num_commits: int = 1000):
    # loop through last 1000 commits
    key = ("last_commit_time", cloned_repo.repo_full_name)
    if key in summary_caches:
        return summary_caches[key]
    last_commit_time = {}
    for commit in tqdm(
        cloned_repo.git_repo.iter_commits(max_count=num_commits),
        desc=f"Getting last commit time for last {num_commits} commits",
        total=num_commits,
    ):
        for file_path in commit.stats.files:
            last_commit_time[file_path] = commit.committed_date
    summary_caches[key] = last_commit_time
    return last_commit_time


def recursively_summarize_directory(cloned_repo: ClonedRepo, update_summaries: bool = False):
    key = ("summaries", cloned_repo.repo_full_name)
    if not update_summaries and key in summary_caches:  # let's just read from the cache
        summaries, counts = summary_caches[key]
        return summaries, counts

    last_commit_time = get_last_commit_time(cloned_repo)

    sweep_config = SweepConfig()
    directory = cloned_repo.repo_dir
    descendants_lines_of_code = count_descendants_files_or_lines_of_code(directory, count_lines_of_code=True)
    directory_summaries = {}
    # go in reverse order
    for subdir in tqdm(sorted(descendants_lines_of_code.keys(), key=lambda x: x.count("/"), reverse=True)):
        # check lines of code in directory instead of descendant counts, sometimes there will be a lot of useful logic in a directory but not many files
        if descendants_lines_of_code[subdir] <= 300:
            continue
        logger.info(f"Summarizing {subdir}")
        snippets_in_subdir = []
        for file_path in os.listdir(os.path.join(cloned_repo.repo_dir, subdir)):
            if os.path.isdir(os.path.join(cloned_repo.repo_dir, subdir, file_path)):
                continue
            try:
                if not is_actual_code_file(
                    os.path.join(cloned_repo.repo_dir, subdir),
                    os.path.join(cloned_repo.repo_dir, subdir, file_path),
                    sweep_config,
                ):
                    continue
                file_contents = open(os.path.join(cloned_repo.repo_dir, subdir, file_path)).read()
                if file_contents.count("\n") > 5000:  # decent filter for now
                    continue
                snippets_in_subdir.append(
                    Snippet(
                        content=file_contents,
                        start=0,
                        end=file_contents.count("\n") + 1,
                        file_path=file_path,
                    )
                )
            except Exception:
                continue

        def snippet_cmp(x):
            return (
                x.file_path.endswith("README.md"),
                x.file_path.endswith(".md"),
                x.file_path.endswith(".rst"),
                last_commit_time.get(file_path, 0),
                x.file_path,
            )

        # put readme first, then md files, then rst, then commit date, then others
        snippets_in_subdir = sorted(snippets_in_subdir, key=snippet_cmp, reverse=True)
        # approximate context for snippets rather than naive slicing
        snippets_in_subdir = pack_items_for_prompt(
            iterable=snippets_in_subdir,
            string_function=lambda snippet: snippet.get_snippet(False, False),
            token_limit=50_000,
        )
        # if there's nothing in the directory, don't summarize
        # there was a bug in summarize_directory where it would summarize the directory even if there were no snippets and the cache was wrong
        if not snippets_in_subdir:
            continue
        # removed mute()
        directory_summaries[subdir] = summarize_directory(subdir, snippets_in_subdir, cloned_repo, directory_summaries)
    summary_caches[key] = directory_summaries, descendants_lines_of_code
    return directory_summaries, descendants_lines_of_code


PRIORITIZED_FILES = [
    "README.md",
    "README.rst",
    "README.txt",
    "README",
    "package.json",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "cargo.toml",
    "go.mod",
]


def fetch_all_prioritized_files(cloned_repo: ClonedRepo):
    prioritized_file_contents = {}
    for root, dirs, files in os.walk(cloned_repo.repo_dir):
        for file in files:
            if file in PRIORITIZED_FILES:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, cloned_repo.repo_dir)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if len(content.splitlines()) < 5:
                        continue
                    prioritized_file_contents[relative_path] = content
                except Exception as e:
                    logger.error(f"Error reading file {file_path}: {str(e)}")

    return prioritized_file_contents


# expanded directories
def generate_tree(cloned_repo: ClonedRepo, max_depth: int = 3, max_files: int = 15):
    descendant_counts = count_descendants_files_or_lines_of_code(cloned_repo.repo_dir)
    root = Node(os.path.basename(cloned_repo.repo_dir))

    def add_children(parent, path, depth=0):
        if depth >= max_depth:
            relative_path = path.removeprefix(cloned_repo.repo_dir).lstrip("/")
            try:
                parent.name += f"/ ({descendant_counts[relative_path]} files)"
            except Exception:
                pass
            return
        directories = []
        files = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                if item not in [".git", "node_modules", ".venv", "build", "venv"]:
                    directories.append(item)
            else:
                files.append(item)

        for directory in sorted(directories):
            child = Node(directory, parent=parent)
            add_children(child, os.path.join(path, directory), depth + 1)

        sorted_files = sorted(
            files,
            key=lambda x: (
                PRIORITIZED_FILES.index(x) if x in PRIORITIZED_FILES else 1000,
                x,
            ),
        )
        if depth == 0 or any(x.split("/")[-1] in PRIORITIZED_FILES for x in sorted_files):  # For root directories
            for file in sorted_files:
                Node(file, parent=parent)
        else:
            for i, file in enumerate(sorted_files):
                if i < max_files:
                    Node(file, parent=parent)
                elif i == max_files:
                    remaining = len(sorted_files) - max_files
                    Node(f"... {remaining} more files", parent=parent)
                    break

    add_children(root, cloned_repo.repo_dir)

    tree_string = ""
    for pre, _, node in RenderTree(root):
        tree_string += f"{pre}{node.name}\n"

    return tree_string


frameworks_format_prompt = """Follow this XML-based format:

<answer>
<summary>
Summary of the repo's purpose and its contents. Then list all significant directories and subdirectories and their purpose.
</summary>

<stack>
Frontend (path/to/directory):
- Languages: Languages used in descending order of frequency
- Frameworks:
    - Framework for purpose
    [list all frameworks used, such as for components, styling, etc.]
- Testing:
    - Framework for testing, mocks, etc.

Backend (path/to/directory):
- Languages: Languages used in descending order of frequency
- Frameworks:
    - Framework for purpose
    [list all frameworks used, such as for routing, database, authentication, caching, observability etc.]
- Testing:
    - Framework for testing, mocks, etc.

[repeat for mobile, infrastructure, jobs, microservices, and any other miscellaneous tools and relevant third-party services etc.]
</stack>
</answer>"""

frameworks_system_prompt = (
    """You are an expert at summarizing the tooling and frameworks used in a project.

For each project of the directory, such as the frontend, mobile, backend or microservices etc., list out all languages and frameworks used in the source code, their corresponding purpose and any frameworks used for their testing.

"""
    + frameworks_format_prompt
)


def summarize_frameworks(
    cloned_repo: ClonedRepo,
):
    key = ("frameworks", cloned_repo.repo_full_name, "v0.0")
    if key in summary_caches:
        return summary_caches[key]
    context = ""
    tree = generate_tree(cloned_repo)
    context += tree
    prioritized_file_contents = fetch_all_prioritized_files(cloned_repo)
    for file_path, content in prioritized_file_contents.items():
        context += f"\n\nFile: {file_path}\n\n<file_contents>\n{content}\n</file_contents>\n\n"

    response = call_llm(
        frameworks_system_prompt,
        context + "\n\n" + frameworks_format_prompt,
        model=LATEST_CLAUDE_MODEL,
    )
    response = extract_xml_tag(response, "answer")
    summary_caches[key] = response, tree
    return response, tree


if __name__ == "__main__":
    from sweepai.core.github_utils import MockClonedRepo
    from sweepai.search.query.lexical_search import prepare_lexical_search_index

    REPO = os.environ.get("REPO")
    org_name, repo_name = REPO.split("/")
    cloned_repo = MockClonedRepo(f"/tmp/{repo_name}", REPO)
    directory = "docs"
    directory = "sweepai/core"
    directory = "sweepai/agents"
    # summarize_frameworks(cloned_repo)

    snippets, lexical_index = prepare_lexical_search_index(
        cloned_repo.repo_dir,
        SweepConfig(),
    )

    print(
        recursively_summarize_directory(
            cloned_repo,
        )
    )
