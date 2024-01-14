import spacy
from database.models import SupportedLanguage
from exceptions import PipelineDoesNotExist


loaded_models: dict[SupportedLanguage.Index, spacy.Language] = dict()

try:
    loaded_models[SupportedLanguage.Index.Deutsch] = spacy.load("de_core_news_lg")
except IOError as e:
    logging.error(f'Error loading spaCy language model: {e}')


class ModelLoader:
    @staticmethod
    def load(lang: SupportedLanguage.Index) -> spacy.Language:
        if lang not in loaded_models:
            raise PipelineDoesNotExist(lang.name)
        return loaded_models[lang]
