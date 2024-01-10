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
        pipeline_name = 'de_core_news_sm'

        try:
            spacy.load("de_core_news_sm")
            import de_core_news_sm
            return de_core_news_sm.load()
        except IOError:
            raise PipelineDoesNotExist(pipeline_name)

    def tokenize(self, sentence: str) -> List[TokenizeResult]:
        doc = self.provider(sentence)

        result: list[TokenizeResult] = []

        for idx, token in enumerate(doc):
            morph = token.morph.to_dict()
            result.append(TokenizeResult(token.text, token.pos_, morph, idx))
        return result



