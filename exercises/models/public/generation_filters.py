from pydantic import BaseModel


class GenerationFilters(BaseModel):
    generator_ids: list[str] = []
