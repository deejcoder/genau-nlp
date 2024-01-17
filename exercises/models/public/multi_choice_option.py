from pydantic import BaseModel
from .fragment_token import FragmentToken


class MultiChoiceOption(BaseModel):
    text: str = ""
    tokens: list[FragmentToken] = []
