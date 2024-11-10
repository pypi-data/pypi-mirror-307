from sweepai.core.github_utils import ClonedRepo
from sweepai.search.agent.entity_search import EntitiesIndex
from sweepai.search.query.ticket_utils import prep_snippets


def prewarm_search_index(repo_identifier: str):
    repo_full_name, _, branch = repo_identifier.partition(":")
    cloned_repo = ClonedRepo.from_repo_full_name(repo_full_name, branch=branch)
    prep_snippets(
        cloned_repo=cloned_repo,
        query="DUMMY QUERY",
        skip_reranking=True,
    )
    branch = cloned_repo.branch
    # Writes to cache
    EntitiesIndex.from_dir(cloned_repo.repo_dir, key=cloned_repo.cache_key, no_cache=True)
