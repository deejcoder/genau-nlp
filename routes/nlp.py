from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from exceptions import LanguageNotSupported
from services import NplProvider
from database.models import SupportedLanguage


router = APIRouter(
    prefix="/nlp",
    tags=["nlp"],
    responses={404: {"description": "Not Found"}},
)


class Token(BaseModel):
    text: str
    pos: str
    morph: dict[str, str]
    order: int


class TokenizeResponse(BaseModel):
    tokens: list[Token]

    class Config:
        arbitrary_types_allowed = True


@router.post("/tokenize", response_model=TokenizeResponse)
async def generate_tags(sentence: str, language: Optional[str] = None) -> TokenizeResponse:
    npl_provider: NplProvider

    match language:
        case 'de':
            npl_provider = NplProvider(SupportedLanguage.Index.Deutsch)

        case _:
            raise LanguageNotSupported(language)

    tokens = [Token(text=item.text, pos=item.pos, morph=item.morph, order=item.order) for item in npl_provider.tokenize(sentence)]

    return TokenizeResponse(tokens=tokens)


