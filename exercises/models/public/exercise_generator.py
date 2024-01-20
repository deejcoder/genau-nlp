from pydantic import BaseModel, Field


class ExerciseGenerator(BaseModel):
    id: str
    description: str
    exercise_type: str = Field(default="", alias="exerciseType")
