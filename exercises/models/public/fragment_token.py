from pydantic import BaseModel


class FragmentToken(BaseModel):
    text: str
    is_punct: bool = False
