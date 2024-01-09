import spacy
from database.models import SupportedLanguage
from exceptions import PipelineDoesNotExist
from typing import List


class TokenizeResult:
    def __init__(self, text: str, pos: str):
        self.text = text
        self.pos = pos


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

        return [TokenizeResult(token.text, token.pos_) for token in doc]




