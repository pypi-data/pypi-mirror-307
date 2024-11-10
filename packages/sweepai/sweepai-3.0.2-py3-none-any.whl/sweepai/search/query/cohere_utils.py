import backoff
from loguru import logger

from sweepai.config.server import COHERE_API_KEY, VOYAGE_API_KEY
from sweepai.core.entities import Message, Snippet
from sweepai.core.llm.chat import Thread, continuous_llm_calls
from sweepai.dataclasses.search_dataclasses import (
    BaseRerankerResponse,
    BaseRerankerResult,
    Document,
)
from sweepai.utils.cache import file_cache
from sweepai.utils.str_utils import extract_objects_from_string
from sweepai.utils.timer import Timer


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=3,
    jitter=backoff.random_jitter,
)
@file_cache()
def cohere_rerank_call(
    query: str,
    documents: list[str],
    model="rerank-english-v3.0",
    **kwargs,
):
    from cohere import Client

    # Cohere API call with caching
    co = Client(COHERE_API_KEY)
    try:
        return co.rerank(model=model, query=query, documents=documents, **kwargs)
    except Exception as e:
        logger.error(f"Cohere rerank failed: {e}")
        raise e


@file_cache()
def voyage_rerank_call(query: str, documents: list[str], model="rerank-1", **kwargs):
    from voyageai import Client

    vo = Client(api_key=VOYAGE_API_KEY)
    return vo.rerank(query, documents, model=model, **kwargs)


reranking_system_prompt = """You are a powerful code search engine. You must order the list of code blocks from the most relevant to the least relevant to the user's query."""

user_prompt = """
# Code blocks to rank:
{documents}
{directory_summary_string}
# User query:
<query>
{query}
</query>

We are currently ranking code blocks of type {code_block_type}.
- source: This is the source code of the software.
- tests: These are the test files in the repository.
- tools: These are tool configurations and scripts used to build, deploy, or manage the software.
- dependencies: These are dependency configurations. They specify the external libraries and packages required by the software.
- docs: These are documentation files. They provide information and instructions about the software.

# Guidelines:
1. Categorize the relevance of each code block as high, low, or irrelevant. The relevance score should be based on how well the code block answers the user query.

2. Ranking Definition:
- "high": The code block is relevant to the user query and important in answering the user query. It is okay if there are multiple high relevance, or no high relevance.
- "low": The code block is not directly related to the user query, such that it can be discarded if there are better options.
- "irrelevant": The code block is completely unrelated to the user query and should be discarded.

3. There may not always be a code block that directly answers the user query ("high" relevance). There may also not be a code block that is "low" relevance. In this case mark the rest as irrelevant.

4. For ranking, you may look at files given explicitly in the list and sometimes files not given but are relevant to the query from the context of the given code blocks.
    a. For the file paths explicitly mentioned, the <file_path> must perfectly reference the provided <file_path> tags within <code_block>.
    b. If you find highly relevant references to some file paths not in the list of code blocks given, the <file_path> tag should have the path to the file (you can figure this out from the context. If you are unsure, just ignore the file.). Downstream logic will take care of disambiguating such files.

You must now rank the code blocks based on relevance to the user query.

# Response Instructions:

Provide the search results in order of relevance, with the most relevant result at the beginning.
<search_result>
<file_path>[THE FILE PATH OF THE CODE BLOCK]</file_path>
<relevance_score>[ONE OF] high, low, irrelevant</relevance_score>
</search_result>
... # RANK ALL OF THE CODE BLOCKS"""

document_format = """<code_block>
  <file_path>{file_path}</file_path>
  <code_block_content>
  {document_contents}
  </code_block_content>
</code_block>"""


def convert_categorical_scores_to_float(scores: list[str]) -> dict[float]:
    # interpolate the scores to a float between 0 and 1
    # high = from 0.7 to 1
    # low = from 0.1 to 0.2
    # irrelevant = from 0 to 0.1
    number_of_highs = scores.count("high")
    number_of_lows = scores.count("low")
    number_of_irrelevants = scores.count("irrelevant")
    last_high_index = scores.index("high") if "high" in scores else 0
    last_low_index = scores.index("low") if "low" in scores else 0
    last_irrelevant_index = scores.index("irrelevant") if "irrelevant" in scores else 0
    float_scores = []
    for idx, score in enumerate(scores):
        if score == "high":
            offset = (idx - last_high_index) / number_of_highs
            interpolated_high_score = 1.0 - (0.3 * offset)
            interpolated_high_score = round(interpolated_high_score, 2)
            float_scores.append(interpolated_high_score)
        elif score == "low":
            offset = (idx - last_low_index) / number_of_lows
            interpolated_low_score = 0.2 - (0.1 * offset)
            interpolated_low_score = round(interpolated_low_score, 2)
            float_scores.append(interpolated_low_score)
        elif score == "irrelevant":
            offset = (idx - last_irrelevant_index) / number_of_irrelevants
            interpolated_irrelevant_score = 0.1 - (0.1 * offset)
            interpolated_irrelevant_score = round(interpolated_irrelevant_score, 2)
            float_scores.append(interpolated_irrelevant_score)
    return float_scores


def llm_rerank_call(
    query: str,
    documents: list[Document],
    most_relevant_snippet_per_file_path: dict[str, Snippet],
    **kwargs,
):
    search_results = []
    formatted_documents = "\n".join(
        [
            document_format.format(
                index=index,
                document_contents=document.content,
                file_path=document.snippet_denotation,
            )
            for index, document in enumerate(documents)
        ]
    )
    directory_summary_string = ""
    if kwargs.get("all_directory_summaries", dict()):
        all_directory_summaries = kwargs["all_directory_summaries"]
        sorted_directory_summaries = sorted(list(all_directory_summaries.items()), key=lambda x: x[0])
        directory_summary_string = "Here is a summary of the directories where the below code blocks were found:\n\n"
        directory_summary_string += "\n\n".join(
            [
                f"Here is a summary of the {subdir_name} subdirectory:\n{directory_summary}"
                for subdir_name, directory_summary in sorted_directory_summaries
            ]
        )
    code_block_type: str = kwargs.get("code_block_type")
    assert code_block_type, "Code block type must be provided"
    formatted_user_prompt = user_prompt.format(
        query=query,
        documents=formatted_documents,
        directory_summary_string=directory_summary_string,
        code_block_type=code_block_type,
    )
    formatted_user_prompt = formatted_user_prompt.strip()
    messages = [
        Message(
            role="system",
            content=reranking_system_prompt.format(code_block_type=code_block_type),
        )
    ]
    thread = Thread(messages=messages)
    with Timer():
        try:
            # for same query, 10k context:
            # gpt-4o-mini takes ~10s
            # haiku takes 4.5s
            search_results = continuous_llm_calls(
                username=kwargs.get("username", "test_user"),
                content=formatted_user_prompt,
                thread=thread,
                stop_sequences=[
                    "irrelevant</relevance_score>",
                    "low</relevance_score>",
                ],
                MAX_CALLS=1,
                verbose=False,
                # can experiment with Claude 3.5 Sonnet later
            )
            if search_results.endswith("</relevance_score>"):
                search_results += "\n</search_result>"
        except Exception as e:
            logger.error(f"LLM rerank failed with exception {e} for query {query}")
            search_results = ""
    reranker_results = parse_search_results_from_string(
        search_results=search_results,
        code_block_type=code_block_type,
        documents=documents,
        most_relevant_snippet_per_file_path=most_relevant_snippet_per_file_path,
    )
    # Ignored for now
    # logger.debug(f"Reranking {code_block_type} for query {query} with results {reranker_results}")
    return reranker_results


def parse_search_results_from_string(
    search_results: str,
    code_block_type: str,
    documents: list[Document],
    most_relevant_snippet_per_file_path: dict[str, Snippet],
) -> BaseRerankerResponse:
    search_objects, failed_extraction = extract_objects_from_string(
        search_results,
        "search_result",
        ["file_path", "relevance_score"],
        include_closing_tag=False,
    )
    reranker_results = BaseRerankerResponse(results=[])
    if not failed_extraction:
        relevance_scores = []
        for llm_search_response_object in search_objects:
            relevance_score = llm_search_response_object["relevance_score"]
            relevance_scores.append(relevance_score)
        float_relevance_scores = convert_categorical_scores_to_float(relevance_scores)
        for llm_search_response_object, float_relevance_score in zip(search_objects, float_relevance_scores):
            try:
                # clean this up to use most relevant snippet per file path
                for index, document in enumerate(documents):
                    if document.snippet_denotation == llm_search_response_object["file_path"]:
                        reranker_results.results.append(
                            BaseRerankerResult(
                                snippet_denotation=documents[index].snippet_denotation,
                                relevance_score=float_relevance_score,
                            )
                        )
                        break
                else:
                    if llm_search_response_object["file_path"] in most_relevant_snippet_per_file_path:
                        reranker_results.results.append(
                            BaseRerankerResult(
                                snippet_denotation=most_relevant_snippet_per_file_path[
                                    llm_search_response_object["file_path"]
                                ].denotation,
                                relevance_score=float_relevance_score,
                            )
                        )
            except Exception as e:
                logger.error(
                    f"Failed to parse code block {llm_search_response_object['file_path']} with exception {e}, trying just the file path"
                )
                original_index = next(
                    (
                        index
                        for index, document in enumerate(documents)
                        if document.snippet_denotation.startswith(llm_search_response_object["file_path"])
                    ),
                    None,
                )
                if original_index is None:
                    logger.error(f"Failed to find code block {llm_search_response_object['file_path']} in documents")
                    continue
                reranker_results.results.append(
                    BaseRerankerResult(
                        snippet_denotation=documents[original_index].snippet_denotation,
                        index=original_index,
                        relevance_score=float_relevance_score,
                    )
                )
    # add test case for this
    if (code_block_type == "source" or code_block_type == "tests") and len(reranker_results.results) == 0:
        reranker_results.results.append(
            BaseRerankerResult(snippet_denotation=documents[0].snippet_denotation, relevance_score=1)
        )
    return reranker_results


if __name__ == "__main__":
    query = "When is Apple's conference call scheduled?"
    documents = [
        Document(
            snippet_denotation="The Mediterranean Diet",
            content="The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
        ),
        Document(
            snippet_denotation="Photosynthesis in Plants",
            content="Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
        ),
        Document(
            snippet_denotation="20th-century Innovations",
            content="20th-century innovations, from radios to smartphones, centered on electronic advancements.",
        ),
        Document(
            snippet_denotation="Rivers",
            content="Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
        ),
        Document(
            snippet_denotation="Latest News",
            content="Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
        ),
        Document(
            snippet_denotation="Shakespeare's Works",
            content="Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature.",
        ),
    ]

    reranking = llm_rerank_call(query, documents)
    for r in reranking.results:
        print(f"Document: {r.file_path}")
        print(f"Relevance Score: {r.relevance_score}")
