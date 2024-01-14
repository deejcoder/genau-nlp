from fastapi import APIRouter
from pydantic import BaseModel
from database.models import ExerciseGeneratorType
from exercises import generate_exercises, MultiChoiceExercise
import exercises.generators

router = APIRouter(
    prefix="/exercises/generate",
    tags=["exercises"],
    responses={404: {"description": "Not Found"}},
)


class MultiChoiceResponse(BaseModel):
    sentence: str
    answer: str
    distractors: list[str]


@router.post("/multi_choice", response_model=list[MultiChoiceResponse])
def generate_multi_choice_exercises(sentence: str):
    generated_exercises = generate_exercises(ExerciseGeneratorType.Index.MultiChoice, exercises.generators, sentence)

    response = []
    for ex in generated_exercises:
        if not isinstance(ex, MultiChoiceExercise):
            continue

        response.append(MultiChoiceResponse(sentence=ex.sentence, answer=ex.answer, distractors=ex.distractors))

    return response
