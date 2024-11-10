from __future__ import annotations

from typing import Callable

from jinja2 import BaseLoader, ChainableUndefined, Environment, StrictUndefined

from sweepai.config.server import DEV
from sweepai.core.entities import Snippet


class EnvironmentWithDecorator(Environment):
    def add_filter(self, filter_func):
        self.filters[filter_func.__name__] = filter_func
        return filter_func


env = EnvironmentWithDecorator(loader=BaseLoader(), undefined=StrictUndefined if DEV else ChainableUndefined)

env.globals.update(
    {
        "enumerate": enumerate,
    }
)

env.filters.update(
    {
        "enumerate": enumerate,
        "list": lambda values: "\n".join([f"- {value}" for value in values]),
        "wrap_xml": lambda value, tag: f"<{tag}>\n{value}\n</{tag}>",
        "wrap_xml_if_non_empty": lambda value, tag: value and f"<{tag}>\n{value}\n</{tag}>" or "",
    }
)


@env.add_filter
def render_snippets(snippets: list[Snippet], EXPAND_SIZE: int = 100):
    return "\n".join([snippet.render(i, EXPAND_SIZE=EXPAND_SIZE) for i, snippet in enumerate(snippets)])


def ordered_dedup(lst: list[str]):
    result = []
    seen = set()
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


class Prompt:
    def __init__(
        self,
        template_string: str,
        strip: bool = True,
        globals: list[Callable] = [],
        filters: list[Callable] = [],
        constants: dict[str, str] = {},
    ):
        for global_func in globals:
            env.globals[global_func.__name__] = global_func
        for filter_func in filters:
            env.filters[filter_func.__name__] = filter_func
        template_string = template_string.strip("\n") if strip else template_string
        self.template = env.from_string(template_string)
        self.constants = constants

    def render(self, strip: bool = True, **kwargs) -> str:  # written this way for backwards compatibility with format
        # ensure uniqueness and completeness of kwargs
        result = self.template.render({**self.constants, **kwargs})
        return result.strip("\n") if strip else result
