from dataclasses import dataclass

from sweepai.dataclasses.use_cases import UseCase


@dataclass
class ChatAgentContext:
    use_case: UseCase = "ticket"
    history: str = ""  # for ci history
