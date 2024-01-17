from database.models import ExerciseGeneratorType
from typing import Callable, Any


class Generator:
    def __init__(self, g_id: str, generator: Callable, path: str, description: str, exercise_type: ExerciseGeneratorType,
                 pattern: list[dict[str, Any]]):
        self.g_id = g_id
        self.func = generator
        self.path = path
        self.description = description
        self.exercise_type = exercise_type
        self.pattern = pattern
