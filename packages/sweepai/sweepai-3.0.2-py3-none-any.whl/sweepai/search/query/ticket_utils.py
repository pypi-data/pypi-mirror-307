import concurrent.futures
import copy
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from tqdm import tqdm

from sweepai.config.client import SweepConfig, get_blocked_dirs
from sweepai.core.entities import Snippet
from sweepai.core.github_utils import ClonedRepo
from sweepai.dataclasses.search_dataclasses import Document
from sweepai.dataclasses.separated_snippets import SeparatedSnippets
from sweepai.o11y.posthog_trace import posthog_trace
from sweepai.search.query.cohere_utils import llm_rerank_call
from sweepai.search.query.lexical_search import (
    compute_vector_search_scores,
    prepare_lexical_search_index,
    search_index,
)
from sweepai.search.query.multi_query import generate_multi_queries
from sweepai.utils.str_utils import pack_items_for_prompt
from sweepai.utils.streamable_functions import streamable
from sweepai.utils.timer import Timer

# the order here matters as the first match is used
code_snippet_separation_features = {
    "tools": {
        "prefix": [
            ".git/",
            ".github/",
            ".circleci/",
            ".travis/",
            ".jenkins/",
            "scripts/",
            "script/",
            "bin/",
        ],
        "suffix": [
            ".gitignore",
            ".dockerignore",
            "Dockerfile",
            "Makefile",
            "Rakefile",
            "Procfile",
            ".sh",
            ".bat",
            ".cmd",
        ],
        "substring": [],
    },
    "junk": {  # we will discard this and not show it to the LLM
        "prefix": [
            "node_modules/",
            ".venv/",
            "build/",
            "venv/",
            "patch/",
            "target/",
            "bin/",
            "obj/",
        ],
        "suffix": [
            ".cache",
            ".gradle",
            ".mvn",
            ".settings",
            ".lock",
            ".log",
            ".tmp",
            ".tmp/",
            ".tmp.lock",
            ".tmp.lock/",
        ],
        "substring": [
            ".egg-info",
            "package-lock.json",
            "yarn.lock",
            ".cache",
            ".gradle",
            ".mvn",
        ],
    },
    "dependencies": {
        "prefix": [".", "config/", ".github/", "vendor/"],
        "suffix": [
            ".cfg",
            ".ini",
            ".po",
            "package.json",
            ".toml",
            ".yaml",
            ".yml",
            "LICENSE",
            ".lock",
        ],
        "substring": [
            "requirements",
            "pyproject",
            "Gemfile",
            "Cargo",
            "pom.xml",
            "build.gradle",
        ],
    },
    "docs": {
        "prefix": ["doc", "example", "README", "CHANGELOG"],
        "suffix": [".txt", ".rst", ".md", ".html", ".1", ".adoc", ".rdoc"],
        "substring": ["docs/", "documentation/"],
    },
    "tests": {
        "prefix": ["tests/", "test/", "spec/"],
        "suffix": [
            ".spec.ts",
            ".spec.js",
            ".test.ts",
            ".test.js",
            "_test.py",
            "_test.ts",
            "_test.js",
            "_test.go",
            "Test.java",
            "Tests.java",
            "Spec.java",
            "Specs.java",
            "_spec.rb",
            "_specs.rb",
            ".feature",
            "cy.ts",
            "cy.js",
        ],
        "substring": [
            "tests/",
            "test/",
            "/test",
            "_test",
            "rspec",
            ".test",
            "testdata/",
            "e2e/",
        ],
    },
}
# otherwise it's tagged as source
# we can make a config category later for css, config.ts, config.js. so far config files aren't many.

type_to_percentile_floor = {  # lower gets more snippets
    "tools": 0.3,
    "dependencies": 0.3,
    "docs": 0.3,
    "tests": 0.3,
    "source": 0.15,  # very low floor for source code
}

# set this to 0.2 because 0.1 means irrelevant in previous ranking steps
type_to_score_floor = {
    "tools": 0.2,
    "dependencies": 0.2,
    "docs": 0.2,
    "tests": 0.2,
    "source": 0.2,
}

type_to_result_count = {
    "tools": 5,
    "dependencies": 5,
    "docs": 5,
    "tests": 15,
    "source": 30,
}

rerank_count = {
    "tools": 10,
    "dependencies": 10,
    "docs": 30,
    "tests": 30,
    "source": 50,  # have to decrease to 30 for Voyage AI
}


def clamp_values(d: dict, max_value: float = 0.05) -> dict:
    if not d:
        return {}
    max_val = max(d.values())
    if max_val <= 0:
        return {k: 0 for k in d}
    return {k: min(max_value, max(0, v * max_value / max_val)) for k, v in d.items()}


def separate_snippets_by_type(snippets: list[Snippet]) -> SeparatedSnippets:
    separated_snippets = SeparatedSnippets()
    for snippet in snippets:
        for type_name, separation in code_snippet_separation_features.items():
            if (
                any(snippet.file_path.startswith(prefix) for prefix in separation["prefix"])
                or any(snippet.file_path.endswith(suffix) for suffix in separation["suffix"])
                or any(substring in snippet.file_path for substring in separation["substring"])
            ):
                separated_snippets.add_snippet(snippet, type_name)
                snippet.type_name = type_name
                break
        else:
            separated_snippets.add_snippet(snippet, "source")
    return separated_snippets


def apply_adjustment_score(
    snippet_path: str,
    old_score: float,
):
    snippet_score = old_score
    file_path, *_ = snippet_path.rsplit(":", 1)
    file_path = file_path.lower()
    # Penalize numbers as they are usually examples of:
    # 1. Test files (e.g. test_utils_3*.py)
    # 2. Generated files (from builds or snapshot tests)
    # 3. Versioned files (e.g. v1.2.3)
    # 4. Migration files (e.g. 2022_01_01_*.sql)
    base_file_name = file_path.split("/")[-1]
    if not base_file_name:
        return 0
    num_numbers = sum(c.isdigit() for c in base_file_name)
    snippet_score *= (1 - 1 / len(base_file_name)) ** num_numbers
    return snippet_score


NUM_SNIPPETS_TO_RERANK = 100
VECTOR_SEARCH_WEIGHT = 2


@streamable
def multi_get_top_k_snippets(
    cloned_repo: ClonedRepo,
    queries: list[str],
    k: int = 15,
    do_not_use_file_cache: bool = False,  # added for review_pr
    use_repo_dir: bool = False,
    seed: str = "",  # for caches
    globs: list[str] = ["**/*"],
):
    """
    Handles multiple queries at once now. Makes the vector search faster.
    """
    yield "Fetching configs...", [], [], []
    sweep_config: SweepConfig = SweepConfig()
    blocked_dirs = get_blocked_dirs(cloned_repo.github_repo)
    sweep_config.exclude_dirs += blocked_dirs
    # repository_directory = cloned_repo.cached_dir
    # if use_repo_dir:
    # We keep going back and forth between the cached_dir and the repo_dir. I set it to be repo_dir
    # because cached_dir was pointing to main and we were on a branch
    repository_directory = cloned_repo.repo_dir
    with Timer() as timer:
        for message, snippets, lexical_index in prepare_lexical_search_index.stream(
            repository_directory,
            sweep_config,
            do_not_use_file_cache=do_not_use_file_cache,
            seed=seed,
            globs=globs,
        ):
            yield message, [], snippets, []
        if len(snippets) == 0:
            yield "No snippets found for index", [], [], []
            return
        logger.info(f"Lexical indexing took {timer.time_elapsed} seconds")
        for snippet in snippets:
            snippet.file_path = snippet.file_path[len(cloned_repo.repo_dir) + 1 :]
        yield "Searching lexical index...", [], snippets, []
        with Timer() as timer:
            content_to_lexical_score_list = [search_index(query, lexical_index) for query in queries]
        logger.info(f"Lexical search took {timer.time_elapsed} seconds")

    # with Timer() as timer:
    #     _ = FilesSummarizer(cloned_repo=cloned_repo)
    logger.info(f"File summaries took {timer.time_elapsed} seconds")

    yield "Finished lexical search and file summaries, performing vector search...", [], snippets, []

    with Timer() as timer:
        for message, files_to_scores_list in compute_vector_search_scores.stream(queries, snippets):
            yield message, [], snippets, []
    logger.info(f"Vector search took {timer.time_elapsed} seconds")

    for i, query in enumerate(queries):
        for snippet in tqdm(snippets):
            vector_score = files_to_scores_list[i].get(snippet.denotation, 0.04)
            snippet_score = 0.02
            if snippet.denotation in content_to_lexical_score_list[i]:
                # roughly fine tuned vector score weight based on average score
                # from search_eval.py on 50 test cases May 13th, 2024 on an internal benchmark
                snippet_score = (
                    content_to_lexical_score_list[i][snippet.denotation] + (vector_score * VECTOR_SEARCH_WEIGHT)
                ) / (VECTOR_SEARCH_WEIGHT + 1)
                content_to_lexical_score_list[i][snippet.denotation] = snippet_score
            else:
                content_to_lexical_score_list[i][snippet.denotation] = snippet_score * vector_score
            content_to_lexical_score_list[i][snippet.denotation] = apply_adjustment_score(
                snippet_path=snippet.denotation,
                old_score=content_to_lexical_score_list[i][snippet.denotation],
            )
    ranked_snippets_list = [
        sorted(
            snippets,
            key=lambda snippet: content_to_lexical_score[snippet.denotation],
            reverse=True,
        )[:k]
        for content_to_lexical_score in content_to_lexical_score_list
    ]
    yield "Finished hybrid search, currently performing reranking...", ranked_snippets_list, snippets, content_to_lexical_score_list


@streamable
def get_top_k_snippets(
    cloned_repo: ClonedRepo,
    query: str,
    k: int = 15,
    do_not_use_file_cache: bool = False,  # added for review_pr
    use_repo_dir: bool = False,
    seed: str = "",
    *args,
    **kwargs,
):
    # Kinda cursed, we have to rework this
    for (
        message,
        ranked_snippets_list,
        snippets,
        content_to_lexical_score_list,
    ) in multi_get_top_k_snippets.stream(
        cloned_repo,
        [query],
        k,
        do_not_use_file_cache=do_not_use_file_cache,
        use_repo_dir=use_repo_dir,
        seed=seed,
        *args,
        **kwargs,
    ):
        yield message, (ranked_snippets_list[0] if ranked_snippets_list else []), snippets, (
            content_to_lexical_score_list[0] if content_to_lexical_score_list else []
        )


def get_pointwise_reranked_snippet_scores(
    query: str,
    snippets: list[Snippet],
    snippet_scores: dict[str, float],
    directory_summaries: dict,
    code_block_type: str,
    NUM_SNIPPETS_TO_RERANK=100,
):
    rerank_scores = copy.deepcopy(snippet_scores)

    sorted_snippets = sorted(
        snippets,
        key=lambda snippet: rerank_scores[snippet.denotation],
        reverse=True,
    )

    MAX_RERANKED_SNIPPETS = 20  # ceiling on the number of snippets to rerank
    snippet_representations: list[Document] = []
    # used for snippets that are not the current set of top snippets.
    valid_file_paths = set()
    most_relevant_snippet_per_file_path = dict()
    for snippet in sorted_snippets:
        if snippet.denotation not in valid_file_paths:
            valid_file_paths.add(snippet.file_path)
            most_relevant_snippet_per_file_path[snippet.file_path] = snippet

    all_directory_summaries = dict()
    for snippet in sorted_snippets[:MAX_RERANKED_SNIPPETS]:
        representation = f"{snippet.get_snippet(add_lines=False, add_ellipsis=False)}"
        # subdirs are all possible parent directories of the snippet
        subdir_names = []
        for subdir_slice in range(1, len(snippet.file_path.split("/"))):
            subdir_names.append("/".join(snippet.file_path.split("/")[:subdir_slice]))
        for subdir in subdir_names:
            if subdir in directory_summaries:
                # check the cache directly
                directory_summary = directory_summaries[subdir]
                if directory_summary in all_directory_summaries:
                    continue
                all_directory_summaries[subdir] = directory_summary
        snippet_representations.append(Document(snippet_denotation=snippet.denotation, content=representation))
    # 12k takes ~3s and can rank 10 items
    # 3k still takes ~3s and can rank 6 items, the bottleneck is TTFT
    # rest of pipeline is .7s
    snippet_representations = pack_items_for_prompt(
        iterable=snippet_representations,
        string_function=lambda x: x.snippet_denotation + x.content,
        token_limit=12_000,
    )
    NUM_SNIPPETS_TO_RERANK = len(snippet_representations)
    logger.info(f"NUM_SNIPPETS_TO_RERANK: {NUM_SNIPPETS_TO_RERANK}")

    # this needs to happen before we update the scores with the (higher) Cohere scores
    snippet_denotations = set(snippet.denotation for snippet in sorted_snippets)
    len(snippet_denotations)

    MAX_VALUE = 0.05
    new_snippet_scores = clamp_values(
        {
            snippet_denotation: v
            for snippet_denotation, v in rerank_scores.items()
            if snippet_denotation in snippet_denotations
        },
        MAX_VALUE,
    )

    response = llm_rerank_call(
        query=query,
        documents=snippet_representations,
        all_directory_summaries=all_directory_summaries,
        code_block_type=code_block_type,
        most_relevant_snippet_per_file_path=most_relevant_snippet_per_file_path,
    )
    for result_document in response.results:
        new_snippet_scores[result_document.snippet_denotation] = apply_adjustment_score(
            snippet_path=result_document.snippet_denotation,
            old_score=result_document.relevance_score,
        )

    # override score with Cohere score
    for snippet in sorted_snippets[:NUM_SNIPPETS_TO_RERANK]:
        if snippet.denotation in new_snippet_scores:
            snippet.score = new_snippet_scores[snippet.denotation]
    return new_snippet_scores


def process_snippets(type_name, *args, **kwargs):
    # not ideal but written this way to support concurrent.futures and for loop
    snippets_subset = args[1] if len(args) >= 2 else kwargs.get("snippets", [])
    if not snippets_subset:
        return type_name, {}
    return type_name, get_pointwise_reranked_snippet_scores(*args, **kwargs)


@streamable
@posthog_trace
def multi_prep_snippets(
    cloned_repo: ClonedRepo,
    queries: list[str],
    k: int = 15,
    skip_reranking: bool = False,  # This is only for pointwise reranking
    skip_pointwise_reranking: bool = False,
    skip_analyze_agent: bool = True,
    NUM_SNIPPETS_TO_RERANK=100,
    globs: list[str] = ["**/*"],
    directory_summaries: dict = {},
    *args,
    **kwargs,
):
    """
    Assume 0th index is the main query.
    """
    if len(queries) > 1:
        logger.info("Using multi query...")
        for (
            message,
            ranked_snippets_list,
            snippets,
            content_to_lexical_score_list,
        ) in multi_get_top_k_snippets.stream(
            cloned_repo,
            queries,
            k * 3,
            globs=globs,  # k * 3 to have enough snippets to rerank
        ):
            yield message, []
        # Use RRF to rerank snippets
        rank_fusion_offset = 0
        content_to_lexical_score = defaultdict(float)
        for i, ordered_snippets in enumerate(ranked_snippets_list):
            for j, snippet in enumerate(ordered_snippets):
                content_to_lexical_score[snippet.denotation] += content_to_lexical_score_list[i][snippet.denotation] * (
                    1 / 2 ** (rank_fusion_offset + j)
                )
        ranked_snippets = sorted(
            snippets,
            key=lambda snippet: content_to_lexical_score[snippet.denotation],
            reverse=True,
        )[:k]
    else:
        for (
            message,
            ranked_snippets,
            snippets,
            content_to_lexical_score,
        ) in get_top_k_snippets.stream(cloned_repo, queries[0], k, globs=globs):
            yield message, ranked_snippets
    separated_snippets = separate_snippets_by_type(snippets)
    yield f"Retrieved top {k} snippets, currently reranking:\n", ranked_snippets
    if not skip_pointwise_reranking and not skip_reranking:
        all_snippets = []
        for type_name, snippets_subset in separated_snippets:
            if len(snippets_subset) == 0:
                continue
            separated_snippets.override_list(
                type_name,
                sorted(
                    snippets_subset,
                    key=lambda snippet: content_to_lexical_score[snippet.denotation],
                    reverse=True,
                )[: rerank_count[type_name]],
            )
        new_content_to_lexical_score_by_type = {}
        with Timer() as timer:
            try:
                with ThreadPoolExecutor(max_workers=len(separated_snippets)) as executor:
                    future_to_type = {
                        executor.submit(
                            process_snippets,
                            type_name,
                            queries[0],
                            snippets_subset,
                            content_to_lexical_score,
                            directory_summaries,
                            type_name,
                            rerank_count[type_name],
                        ): type_name
                        for type_name, snippets_subset in separated_snippets
                    }
                    for future in concurrent.futures.as_completed(future_to_type):
                        type_name = future_to_type[future]
                        new_content_to_lexical_score_by_type[type_name] = future.result()[1]
            except RuntimeError as e:
                # Fallback to sequential processing
                logger.warning(e)
                for type_name, snippets_subset in separated_snippets:
                    new_content_to_lexical_score_by_type[type_name] = process_snippets(
                        type_name,
                        queries[0],
                        snippets_subset,
                        content_to_lexical_score,
                        directory_summaries,
                        type_name,
                        rerank_count[type_name],
                    )[1]
        logger.info(f"Reranked snippets took {timer.time_elapsed} seconds")
        for type_name, snippets_subset in separated_snippets:
            new_content_to_lexical_scores = new_content_to_lexical_score_by_type[type_name]
            for snippet in snippets_subset:
                snippet.score = new_content_to_lexical_scores[snippet.denotation]
            # set all keys of new_content_to_lexical_scores to content_to_lexical_score
            for key in new_content_to_lexical_scores:
                content_to_lexical_score[key] = new_content_to_lexical_scores[key]
            snippets_subset = sorted(
                snippets_subset,
                key=lambda snippet: new_content_to_lexical_scores[snippet.denotation],
                reverse=True,
            )
            separated_snippets.override_list(attribute_name=type_name, new_list=snippets_subset)
            logger.info(f"Reranked {type_name}")
            # cutoff snippets at percentile
            logger.info("Kept these snippets")
            if not snippets_subset:
                continue
            top_score = snippets_subset[0].score
            logger.debug(f"Top score for {type_name}: {top_score}")
            max_results = type_to_result_count[type_name]
            filtered_subset_snippets = []
            for idx, snippet in enumerate(snippets_subset[:max_results]):
                percentile = 0 if top_score == 0 else snippet.score / top_score
                if percentile < type_to_percentile_floor[type_name] or snippet.score <= type_to_score_floor[type_name]:
                    break
                logger.info(f"{idx}: {snippet.denotation} {snippet.score} {percentile}")
                snippet.type_name = type_name
                filtered_subset_snippets.append(snippet)
            logger.info(f"Length of filtered subset snippets for {type_name}: {len(filtered_subset_snippets)}")
            all_snippets.extend(filtered_subset_snippets)
        # if there are no snippets because all of them have been filtered out we will fall back to adding the highest rated ones
        # only do this for source files
        if not all_snippets:
            for type_name, snippets_subset in separated_snippets:
                # only use source files unless there are none in which case use all snippets
                if type_name != "source" and separated_snippets.source:
                    continue
                max_results = type_to_result_count[type_name]
                all_snippets.extend(snippets_subset[:max_results])

        all_snippets.sort(key=lambda snippet: snippet.score, reverse=True)
        ranked_snippets = all_snippets[:k]
        yield "Finished reranking, here are the relevant final search results:\n", ranked_snippets
    else:
        ranked_snippets = sorted(
            snippets,
            key=lambda snippet: content_to_lexical_score[snippet.denotation],
            reverse=True,
        )[:k]
        yield "Finished reranking, here are the relevant final search results:\n", ranked_snippets
    return ranked_snippets


@streamable
def prep_snippets(
    cloned_repo: ClonedRepo,
    query: str,
    k: int = 15,
    skip_reranking: bool = False,
    use_multi_query: bool = False,
    *args,
    **kwargs,
) -> list[Snippet]:
    if use_multi_query:
        queries = [query, *generate_multi_queries(query)]
        yield "Finished generating search queries, performing lexical search...\n", []
    else:
        queries = [query]
    for message, snippets in multi_prep_snippets.stream(cloned_repo, queries, k, skip_reranking, *args, **kwargs):
        yield message, snippets
    return snippets


if __name__ == "__main__":
    import os

    from sweepai.config.server import CACHE_DIRECTORY
    from sweepai.core.github_utils import MockClonedRepo
    from sweepai.utils.timer import Timer

    repo_full_name = os.environ.get("REPO_NAME")  # can test using this # REPO_NAME=sweepai/sweep-internal
    QUERY = os.environ.get("QUERY")  # QUERY="Write unit tests for ClonedRepo in github_utils.py"
    org_name, repo_name = repo_full_name.split("/")
    cloned_repo = MockClonedRepo(
        _repo_dir=f"{CACHE_DIRECTORY}/repos/{org_name}/{repo_name}/base/dev",
        repo_full_name=repo_full_name,
    )

    with Timer() as timer:
        for message, snippets in multi_prep_snippets.stream(cloned_repo, [QUERY], k=15):
            print(message, snippets)
    print("Time taken:", timer.time_elapsed)
