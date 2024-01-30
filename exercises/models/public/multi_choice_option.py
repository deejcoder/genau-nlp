from pydantic import BaseModel, Field
from .fragment_token import FragmentToken


class MultiChoiceOption(BaseModel):
    text: str = ""
    tokens: list[FragmentToken] = []
    correct: bool = Field(default=False, alias="correct")
