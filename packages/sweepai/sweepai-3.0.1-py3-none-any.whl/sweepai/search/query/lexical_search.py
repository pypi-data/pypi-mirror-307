import fnmatch
import multiprocessing
import os
import re
import subprocess
import time
from collections.abc import Iterable

from diskcache import Cache
from loguru import logger
from tantivy import Document, Index, SchemaBuilder
from tqdm import tqdm

from sweepai.config.client import SweepConfig
from sweepai.config.server import CACHE_DIRECTORY
from sweepai.core.entities import Snippet
from sweepai.dataclasses.files import LexicalSearchDocument
from sweepai.o11y.event_logger import posthog
from sweepai.search.agent.files_summarizer import file_summary_cache
from sweepai.search.query.repo_parsing_utils import directory_to_chunks
from sweepai.search.query.vector_db import multi_get_query_texts_similarity
from sweepai.utils.cache import hash_code
from sweepai.utils.streamable_functions import streamable
from sweepai.utils.timer import Timer

token_cache = Cache(f"{CACHE_DIRECTORY}/token_cache")  # we instantiate a singleton, diskcache will handle concurrency
lexical_index_cache = Cache(f"{CACHE_DIRECTORY}/lexical_index_cache")
snippets_cache = Cache(f"{CACHE_DIRECTORY}/snippets_cache")
CACHE_VERSION = "v1.0.17"

# pylint: disable=no-member
schema_builder = SchemaBuilder()
schema_builder.add_text_field("title", stored=True)
schema_builder.add_text_field("body", stored=True)
schema_builder.add_integer_field("doc_id", stored=True)
schema = schema_builder.build()
# pylint: enable=no-member


class CustomIndex:
    def __init__(self, cache_path: str = None):
        os.makedirs(cache_path, exist_ok=True)
        self.index = Index(schema)  # pylint: disable=no-member

    def add_documents(self, documents: Iterable):
        writer = self.index.writer()
        for doc_id, (title, text) in enumerate(documents):
            writer.add_document(Document(title=title, body=text, doc_id=doc_id))  # pylint: disable=no-member
        writer.commit()

    def search_index(self, query: str) -> list[tuple[str, float, dict]]:
        tokenized_query = tokenize_code(query)
        parsed_query = self.index.parse_query(tokenized_query)
        searcher = self.index.searcher()  # for some reason, the first searcher is empty
        for i in range(100):
            searcher = self.index.searcher()
            if searcher.num_docs > 0:
                break
            print(f"Index is empty, sleeping for {0.01 * i} seconds")
            time.sleep(0.01)
        else:
            raise Exception("Index is empty")
        results = searcher.search(parsed_query, limit=200).hits
        return [(searcher.doc(doc_id)["title"][0], score, searcher.doc(doc_id)) for score, doc_id in results]


variable_pattern = re.compile(r"([A-Z][a-z]+|[a-z]+|[A-Z]+(?=[A-Z]|$))")


def tokenize_code(code: str) -> str:
    matches = re.finditer(r"\b\w{2,}\b", code)
    tokens: list[str] = []
    for m in matches:
        text = m.group()
        underscore_matches = text.split("_")
        if len(underscore_matches) > 1:
            tokens.append(text)
        for underscore_match in underscore_matches:
            variable_matches = variable_pattern.findall(underscore_match)
            # if len(variable_matches) > 1:
            #     tokens.append(underscore_match)
            for part in variable_matches:
                if len(part) < 2:
                    continue
                # if more than half of the characters are letters
                # and the ratio of unique characters to the number of characters is less than 5
                if (
                    sum(1 for c in part if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9") > len(part) // 2
                    and len(part) / len(set(part)) < 4
                ):
                    tokens.append(part)
    return " ".join(token.lower() for token in tokens)


def snippets_to_docs(snippets: list[Snippet], len_repo_cache_dir):
    docs = []
    for snippet in snippets:
        docs.append(
            LexicalSearchDocument(
                title=f"{snippet.file_path[len_repo_cache_dir:]}:{snippet.start}-{snippet.end}",
                content=snippet.get_snippet(add_ellipsis=False, add_lines=False),
            )
        )
    return docs


@streamable
def prepare_index_from_snippets(
    snippets: list[Snippet],
    len_repo_cache_dir: int = 0,
    do_not_use_file_cache: bool = False,
    cache_path: str = None,
) -> CustomIndex | None:
    all_docs: list[LexicalSearchDocument] = snippets_to_docs(snippets, len_repo_cache_dir)
    if len(all_docs) == 0:
        posthog.capture(
            "preparing index failed with no docs",
            "no docs found for index",
            properties={
                "cache_path": cache_path,
                "do_not_use_file_cache": do_not_use_file_cache,
                "len_repo_cache_dir": len_repo_cache_dir,
                "len_snippets": len(snippets),
            },
        )
        return None
    index = CustomIndex(cache_path=cache_path)
    yield "Tokenizing documents...", index
    all_tokens = []
    try:
        with Timer() as timer:
            for doc in all_docs:
                all_tokens.append(token_cache.get(doc.content + CACHE_VERSION))
            misses = [i for i, token in enumerate(all_tokens) if token is None]
            num_workers = multiprocessing.cpu_count() // 3
            if misses:
                if num_workers > 1 or len(misses) > 1000:
                    with multiprocessing.Pool(processes=num_workers) as p:
                        missed_tokens = p.map(
                            tokenize_code,
                            tqdm(
                                [all_docs[i].content for i in misses],
                                total=len(misses),
                                desc="Tokenizing documents",
                            ),
                        )
                else:
                    missed_tokens = [tokenize_code(all_docs[i].content) for i in misses]
                for i, token in enumerate(missed_tokens):
                    all_tokens[misses[i]] = token
                    token_cache[all_docs[misses[i]].content + CACHE_VERSION] = token
        logger.debug(f"Tokenizing documents took {timer.time_elapsed} seconds")
        yield "Building lexical index...", index
        all_titles = [doc.title for doc in all_docs]
        with Timer() as timer:
            index.add_documents(tqdm(zip(all_titles, all_tokens), total=len(all_docs), desc="Indexing"))
        logger.debug(f"Indexing took {timer.time_elapsed} seconds")
    except FileNotFoundError as e:
        logger.exception(e)
    yield "Index built", index
    return index


def search_index(query: str, index: CustomIndex):
    """Search the index based on a query.

    This function takes a query and an index as input and returns a dictionary of document IDs
    and their corresponding scores.
    """
    # Create a query parser for the "content" field of the index
    if index:
        results_with_metadata = index.search_index(query)
    else:
        results_with_metadata = []
    # Search the index
    res = {}
    for doc_id, score, _ in results_with_metadata:
        if doc_id not in res:
            res[doc_id] = score
    # min max normalize scores from 0.5 to 1
    if len(res) == 0:
        max_score = 1
        min_score = 0
    else:
        max_score = max(res.values())
        min_score = min(res.values()) if min(res.values()) < max_score else 0
    res = {k: (v - min_score) / (max_score - min_score) for k, v in res.items()}
    return res


SNIPPET_FORMAT = """<file_path>
{file_path}
</file_path>

<file_summary>
{file_summary}
</file_summary>

{contents}"""


# @file_cache(ignore_params=["snippets"])
@streamable
def compute_vector_search_scores(queries: list[str], snippets: list[Snippet]):
    # get get dict of snippet to score
    def get_file_summary_from_cache(snippet: Snippet):
        return file_summary_cache.get(hash_code(snippet.content))

    with Timer() as timer:
        snippet_str_to_contents = {
            snippet.denotation: SNIPPET_FORMAT.format(
                file_path=snippet.file_path,
                file_summary=get_file_summary_from_cache(snippet),
                contents=snippet.get_snippet(add_ellipsis=False, add_lines=False),
            )
            for snippet in snippets
        }
    logger.info(f"Snippet to contents took {timer.time_elapsed:.2f} seconds")
    snippet_contents_array = list(snippet_str_to_contents.values())
    multi_query_snippet_similarities = []
    for (
        message,
        multi_query_snippet_similarities,
    ) in multi_get_query_texts_similarity.stream(queries, snippet_contents_array):
        yield message, multi_query_snippet_similarities
    snippet_denotations = [snippet.denotation for snippet in snippets]
    snippet_denotation_to_scores = [
        {snippet_denotations[i]: score for i, score in enumerate(query_snippet_similarities)}
        for query_snippet_similarities in multi_query_snippet_similarities
    ]
    yield "Vector search scores computed.", snippet_denotation_to_scores
    return snippet_denotation_to_scores


def get_lexical_cache_key(repo_directory: str, commit_hash: str | None = None, seed: str = ""):
    commit_hash = (
        commit_hash
        or subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_directory,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    repo_directory = os.path.basename(repo_directory)
    return f"{repo_directory}_{commit_hash}_{CACHE_VERSION}_{seed}"


@streamable
def prepare_lexical_search_index(
    repo_directory: str,
    sweep_config: SweepConfig,
    do_not_use_file_cache: bool = False,  # choose to not cache results
    seed: str = "",  # used for lexical cache key
    globs: list[str] = ["**/*"],
):
    lexical_cache_key = get_lexical_cache_key(repo_directory, seed=seed)

    yield "Collecting snippets...", [], None
    snippets_results = snippets_cache.get(lexical_cache_key)
    if snippets_results is None:
        snippets, file_list = directory_to_chunks(
            repo_directory, sweep_config, do_not_use_file_cache=do_not_use_file_cache
        )
        snippets_cache[lexical_cache_key] = snippets, file_list
    else:
        snippets, file_list = snippets_results

    if len(snippets) == 0:
        logger.warning("No snippets found for index, repository may be empty")
        yield "No snippets found for index, repository may be empty", [], None
        return [], None

    globs = [glob.replace("/**", "").replace("*/*", "*") for glob in globs]  # /** isn't handled properly by fnmatch
    # snippets get kept if they match any of the globs
    filtered_snippets = [
        snippet
        for snippet in snippets
        if any(fnmatch.fnmatch(name=snippet.file_path[len(repo_directory) :].lstrip("/"), pat=glob) for glob in globs)
    ]

    if len(filtered_snippets) == 0:
        logger.warning("No snippets found for index, probably due to globs being too restrictive")
        yield "No snippets found for index, globs may be too restrictive", [], None
        return [], None

    snippets = filtered_snippets
    yield "Building index...", snippets, None

    index = prepare_index_from_snippets(
        snippets,
        len_repo_cache_dir=len(repo_directory) + 1,
        do_not_use_file_cache=do_not_use_file_cache,
        cache_path=f"{CACHE_DIRECTORY}/lexical_index_cache/{lexical_cache_key}",
    )

    yield "Lexical index built.", snippets, index

    return snippets, index


if __name__ == "__main__":
    repo_directory = os.getenv("REPO_DIRECTORY")
    sweep_config = SweepConfig()
    assert repo_directory
    import time

    start = time.time()
    snippets, index = prepare_lexical_search_index(repo_directory, sweep_config, None)
    breakpoint()  # noqa: T100
    result = search_index("logger export", index)
    print("Time taken:", time.time() - start)
    # print some of the keys
    print(list(result.keys())[:5])
    # print the first 2 result keys sorting by value
    print(sorted(result.items(), key=lambda x: result.get(x, 0), reverse=True)[:5])
