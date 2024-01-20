from pydantic import BaseModel, Field


class GenerationFilters(BaseModel):
    generator_ids: list[str] = Field(default=[], alias="generatorIds")
