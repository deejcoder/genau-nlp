import spacy

from database.models import SupportedLanguage
from services.nlp.model_loader import ModelLoader
from typing import Optional


class NlpBlob:
    def __init__(self, text: str, lang: str):
        self.text = text
        self.model = self._get_model(lang)
        self.doc = self.model(text)

    def _get_model(self, lang: str) -> Optional[spacy.Language]:
        if lang.lower() == "de":
            return ModelLoader.load(SupportedLanguage.Index.Deutsch)
        return None




