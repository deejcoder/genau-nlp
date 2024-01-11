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


class FindSimiliarities(BaseModel):
    word: str
    others: list[str]


class CalculedSimilarity(BaseModel):
    word: str
    other: str
    result: float


class FindSimiliaritiesResponse(BaseModel):
    result: list[CalculedSimilarity]


def get_npl_provider(language: Optional[str] = None):
    match language:
        case 'de':
            return NplProvider(SupportedLanguage.Index.Deutsch)

        case _:
            raise LanguageNotSupported(language)


@router.post("/tokenize", response_model=TokenizeResponse)
async def generate_tags(sentence: str, language: Optional[str] = None) -> TokenizeResponse:
    npl_provider = get_npl_provider(language)

    tokens = [Token(text=item.text, pos=item.pos, morph=item.morph, order=item.order) for item in npl_provider.tokenize(sentence)]

    return TokenizeResponse(tokens=tokens)


@router.post("/find_similarities", response_model=FindSimiliaritiesResponse)
async def find_similarities(word: str, others: str, language: str) -> FindSimiliaritiesResponse:
    # look at transformers
    npl_provider = get_npl_provider(language)
    tokens = npl_provider.tokenize(others)

    npl_result = npl_provider.calculate_word_similarities(word, [token.text for token in tokens])

    results = [CalculedSimilarity(word=result.word, other=result.other, result=result.result) for result in npl_result]
    return FindSimiliaritiesResponse(result=results)
