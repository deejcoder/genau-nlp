from typing import Callable, List
from .sentence_parts import SentenceParts


class MatchingGenerator:
    def __init__(self, g_id: str, generator: Callable, name: str, sentences: List[SentenceParts]):
        self.g_id = g_id
        self.name = name
        self.generator = generator
        self.sentences = sentences
