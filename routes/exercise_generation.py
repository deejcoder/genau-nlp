from fastapi import APIRouter
from database.models import ExerciseGeneratorType
from exercises import generate
from exercises.generation import get_exercise_generators
import exercises.generators
from exercises.models.public import ExerciseGenerator, GenerationFilters, MultiChoiceExercise

router = APIRouter(
    prefix="/exercises/generate",
    tags=["exercise-generation"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/generators", response_model=list[ExerciseGenerator])
def get_generator_list():
    generators = get_exercise_generators(exercises.generators)

    return [ExerciseGenerator(
        id=g.g_id,
        description=g.description,
        exercise_type=g.exercise_type.code) for g in generators]


@router.post("/multi-choice", response_model=list[MultiChoiceExercise])
def generate_multi_choice_exercises(sentence: str, filters: GenerationFilters):
    exercise_type = ExerciseGeneratorType.Index.MultiChoice

    result = generate.generate_exercises(exercise_type, exercises.generators, sentence, filters.generator_ids)

    response = []
    for ex in result:
        if not isinstance(ex, MultiChoiceExercise):
            continue

        response.append(ex)

    return response
