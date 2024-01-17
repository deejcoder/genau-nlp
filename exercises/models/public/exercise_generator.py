from pydantic import BaseModel


class ExerciseGenerator(BaseModel):
    id: str
    description: str
    exercise_type: str
