from datetime import datetime
from github.PullRequest import PullRequest
from loguru import logger
import pytz

from sweepai.ci.fetch_ci import get_ci_failure_logs, get_ci_failures
from sweepai.config.server import FIX_CI_ALLOWLIST
from sweepai.core.github_utils import github_integration
from sweepai.core.llm.chat import LATEST_CLAUDE_MODEL, Thread, continuous_llm_calls
from sweepai.o11y.log_utils import log_to_file
from sweepai.utils.diff import remove_whitespace_changes
from sweepai.utils.format_utils import Prompt
from sweepai.utils.str_utils import extract_all_xml_tags, wildcard_match
from sweepai.utils.ticket_rendering_utils import create_message_marker, create_or_edit_sweeps_github_comment, find_sweeps_github_comment

system_message = "You are a helpful assistant that reviews pull requests and suggests unit tests that should be added to a pull request."

user_message = Prompt("""
Take a look at the following pull request:

<pull_request>
{{ title | wrap_xml('title') }}
{{ body | wrap_xml('body') }}
{{ patch | wrap_xml('patch') }}
</pull_request>

Suggest areas of the code that can be improved, such as adding unit tests for newly created utilities or features. Do not suggest refactors. If there is nothing relevant to suggest, just say "No suggestions."

Respond with this format:

<suggestions>
<suggestion>
[ Example: Add unit tests for function `foo` that tests for the case where `bar` is `baz`. ]
</suggestion>
[... other suggestions if applicable]

If there are no suggestions, just say "No suggestions."
</suggestions>
""")

def generate_auto_suggestions(pull_request: PullRequest) -> list[str]:
    # _pending_runs, _successful_runs, error_runs = get_ci_failures(pull_request)
    # logs_list = get_ci_failure_logs(installation_id, error_runs, pull_request)

    thread = Thread.from_system_message_string(system_message)
    patch = "\n".join([
        f"#### `{pull_request_file.filename}`\n```diff\n{remove_whitespace_changes(pull_request_file.patch)}\n```\n"
        for pull_request_file in pull_request.get_files() if pull_request_file.patch is not None
    ])
    response = continuous_llm_calls(
        username="suggestions", # TODO: use actual username
        thread=thread,
        content=user_message.render(
            title=pull_request.title,
            body=pull_request.body,
            patch=patch,
        ),
        stop_sequences=["</suggestion>"],
        model=LATEST_CLAUDE_MODEL,
    )
    results = extract_all_xml_tags(response, "suggestion")
    return results

# Technically we check with @sweep but @sweepai auto-corrects better
comment_template = Prompt("""
Hey @{{username}}, here {% if suggestions|length == 1 %}is an example{% else %}are examples{% endif %} of how you can ask me to improve this pull request:

{% for suggestion in suggestions %}
<blockquote>
@sweep {{ suggestion.replace('\n', '<br/>') }}
</blockquote>
{% endfor %}

""")

def provide_auto_suggestions(pull_request: PullRequest, tracking_id: str | None = None) -> list[str]:
    username = pull_request.user.login
    
    if not wildcard_match(username, FIX_CI_ALLOWLIST):
        return []
    
    message_marker = create_message_marker("auto_suggestions")

    with log_to_file(f"auto-suggestions-{tracking_id}"):
        logger.info(f"Generating auto-suggestions for {pull_request.number}")
        sweeps_github_comment = find_sweeps_github_comment(pull_request, message_marker)
        if sweeps_github_comment and (datetime.now(pytz.utc) - sweeps_github_comment.updated_at).seconds < 60:
            # If it's been recently edited, debounce. We have this due to check_suite events hammering all at once.
            return []

        suggestions = generate_auto_suggestions(pull_request)

        if not suggestions:
            return []

        # Adding CI to list of suggestions
        org_name, repo_name = pull_request.base.repo.full_name.split("/")
        installation_id = github_integration.get_repo_installation(org_name, repo_name).id

        pending_runs, _successful_runs, error_runs = get_ci_failures(pull_request)
        logs_list = get_ci_failure_logs(installation_id, error_runs, pull_request)

        if logs_list:
            suggestions = [f"Fix the CI errors."] + suggestions

        # Sending to user
        sweeps_github_comment = create_or_edit_sweeps_github_comment(pull_request, comment_template.render(
            username=username,
            suggestions=suggestions,
        ), message_marker=message_marker)
        sweeps_github_comment.create_reaction("+1")
        sweeps_github_comment.create_reaction("-1")
        return suggestions

if __name__ == "__main__":
    from sweepai.core.github_links import parse_url
    from sweepai.core.github_utils import get_github_repo
    pull_request_url = "https://github.com/sweepai/sweep-internal/pull/1315/files"
    parsed_url = parse_url(pull_request_url)

    repo = get_github_repo(f"{parsed_url.org_name}/{parsed_url.repo_name}")
    pull_request = repo.get_pull(parsed_url.pull_request_number)
    print(provide_auto_suggestions(pull_request))
