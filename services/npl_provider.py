import spacy
from database.models import SupportedLanguage
from exceptions import PipelineDoesNotExist
from typing import List


class TokenizeResult:
    def __init__(self, text: str, pos: str, morph: dict, order: int):
        self.text = text
        self.pos = pos
        self.morph = morph
        self.order = order

class SimilarityResult:
    def __init__(self, word: str, other: str, result: float):
        self.word = word
        self.other = other
        self.result = result


doc = spacy.load("de_core_news_lg")


class NplProvider:
    def __init__(self, language: SupportedLanguage.Index):
        self.language = language
        self.provider = self.load_pipeline()

    def load_pipeline(self) -> spacy.Language:
        match self.language:
            case SupportedLanguage.Index.Deutsch:
                return self.load_de_pipeline()

    @staticmethod
    def load_de_pipeline() -> spacy.Language:
        return doc

    def tokenize(self, sentence: str) -> List[TokenizeResult]:
        doc = self.provider(sentence)

        result: list[TokenizeResult] = []

        for idx, token in enumerate(doc):
            morph = token.morph.to_dict()
            result.append(TokenizeResult(token.text, token.pos_, morph, idx))
        return result

    def calculate_word_similarities(self, word: str, others: list[str]) -> list[SimilarityResult]:
        doc_word = self.provider(word)

        result: list[SimilarityResult] = []

        for other in others:
            doc_other = self.provider(other)

            result.append(SimilarityResult(word, other, doc_word.similarity(doc_other)))

        return result





