from dataclasses import dataclass

from sweepai.core.entities import FileChangeRequest
from sweepai.modify.validate.code_validators import CheckResults
from sweepai.search.agent.entity_search import EntitiesIndex


@dataclass
class LLMState:
    request: str
    visited_snippets: set[str]
    visited_questions: set[str]
    visited_ripgrep: set
    ripgrep_queries: set[str]
    viewed_files: set[str]
    entities_index: EntitiesIndex


@dataclass
class ModifyLLMState:
    request: str
    plan: str
    current_task: str
    user_message_index: int
    user_message_index_chat_logger: int
    done_counter: int  # keep track of how many times the submit_task tool has been called
    fcrs: list[FileChangeRequest]
    previous_attempt: str
    changes_per_fcr: list[int]  # how many old/new code pairs there are per fcr
    completed_changes_per_fcr: list[int]  # how many old/new code pairs have been completed per fcr
    attempt_lazy_change: bool  # whether or not we attempt to bypass the llm call and apply old/new code pair directly
    attempt_count: int  # how many times we have attempted to apply the old/new code pair
    visited_set: set[str]
    status_messages: list[str]
    symbol_to_code_map: dict[
        str, str
    ]  # used to provide shortcuts for the llm when it messes up original_code and we provide it the best match
    initial_check_results: dict[str, CheckResults]
