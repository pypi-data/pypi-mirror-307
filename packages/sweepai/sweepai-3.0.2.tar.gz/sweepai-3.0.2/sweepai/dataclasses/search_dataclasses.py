from dataclasses import dataclass


@dataclass
class BaseRerankerResult:
    snippet_denotation: str  # these are the actual contents passed in
    relevance_score: float  # score from 0 to 1

    def __repr__(self) -> str:
        return f"RerankerResult <file_path {self.snippet_denotation}> <relevance_score {self.relevance_score}>"


@dataclass
class BaseRerankerResponse:
    results: list[BaseRerankerResult]  # wrapper for openai to return the results in the correct format

    def __repr__(self) -> str:
        return "\nRerankerResponse\n" + "\n\n".join([result.__repr__() for result in self.results])


@dataclass
class Document:
    snippet_denotation: str
    content: str
