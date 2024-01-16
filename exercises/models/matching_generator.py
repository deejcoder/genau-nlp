from typing import Callable, List
from spacy.tokens import Span


class MatchingGenerator:
    def __init__(self, g_id: str, generator: Callable, name: str, matches: List[Span]):
        self.g_id = g_id
        self.name = name
        self.generator = generator
        self.matches = matches
