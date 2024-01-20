from typing import Optional

import spacy
from spacy.tokens import Token, Span

from database.models import SupportedLanguage
from .model_loader import ModelLoader


class NlpToolkit:

    @classmethod
    def load_model(cls, language: str) -> Optional[spacy.Language]:
        if language.lower() == "de":
            return ModelLoader.load(SupportedLanguage.Index.Deutsch)
        return None

    @classmethod
    def detokenize(cls, tokens: list[Token]) -> str:
        result = ""

        last_token = tokens[-1]

        for token in tokens:
            result += token.text

            # add trailing whitespace?
            if token is not last_token and len(token.whitespace_) != 0:
                result += token.whitespace_

        return result

    @classmethod
    def replace_token(cls, tokens: list[Token], token_to_replace: Token, replace_with: Token) -> list[Token]:
        idx = tokens.index(token_to_replace)

        tokens[idx] = replace_with
        return tokens

    @classmethod
    def replace_token_in_span(cls, span: Span, token_to_replace: Token, replace_with: Token) -> list[Token]:
        tokens = [token for token in span]
        tokens = cls.replace_token(tokens, token_to_replace, replace_with)

        return tokens


