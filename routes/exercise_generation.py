from fastapi import APIRouter
from pydantic import BaseModel
from database.models import ExerciseGeneratorType
from exercises import generate, MultiChoiceExercise
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


class ExerciseList(BaseModel):
    multi_choice: list[MultiChoiceResponse]


class ExerciseGenerator(BaseModel):
    id: str
    description: str
    exercise_type: str


class GenerationFilters(BaseModel):
    generator_ids: list[str]


@router.get("/list", response_model=list[ExerciseGenerator])
def get_generator_list():
    generators = generate.get_exercise_generators(exercises.generators)

    return [ExerciseGenerator(
        id=g.g_id,
        description=g.description,
        exercise_type=g.exercise_type.code) for g in generators]


@router.post("/generate", response_model=ExerciseList)
def generate_exercises(sentence: str, filters: GenerationFilters):
    exercise_type = ExerciseGeneratorType.Index.MultiChoice
    result = generate.generate_exercises(exercise_type, exercises.generators, sentence, filters.generator_ids)

    response = []
    for ex in result:
        if not isinstance(ex, MultiChoiceExercise):
            continue

        response.append(MultiChoiceResponse(sentence=ex.sentence, answer=ex.answer, distractors=ex.distractors))

    return ExerciseList(multi_choice=response)
