from typing import Literal

# I don't like enums because they cause a lot of unexpected errors when used incorrectly
# For example, Enum.VALUE is not of type string and comparisons won't work properly
UseCase = Literal["chat", "ticket", "ci"]
use_cases: list[UseCase] = list(UseCase.__args__)
