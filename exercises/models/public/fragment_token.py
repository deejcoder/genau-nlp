from pydantic import BaseModel, Field


class FragmentToken(BaseModel):
    text: str
    is_punct: bool = Field(default=False, alias="isPunct")
    trailing_whitespace: str = Field(default="", alias="trailingWhitespace")
