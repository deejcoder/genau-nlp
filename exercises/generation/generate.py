import types
from typing import List
from database.models import ExerciseGeneratorType
from ..models import Exercise
from . import get_exercise_generators_by_pattern
from . import get_exercise_generators


def generate_exercises(exercise_type: ExerciseGeneratorType.Index,
                       module: types.ModuleType,
                       sentence: str,
                       generator_ids: list[str]) -> List[Exercise]:
    """
    Generates a random exercise based on the available exercise generators
    :param exercise_type: the abstract type of exercise to generate
    :param module: where to look for exercise generators
    :param sentence: the sentence to base the exercise on
    :param generator_ids: if specified, filters the generators to use when generating exercises
    :return: a generated exercise
    """
    matching_generators = get_exercise_generators_by_pattern(exercise_type, module, sentence)

    if len(matching_generators) == 0:
        return []

    # filter by generators if any have been specified
    # filter out empty strings
    generator_ids = set(filter(lambda g: len(g) > 0, generator_ids))

    if len(generator_ids) > 0:
        matching_generators = list(filter(lambda g: g.g_id in generator_ids, matching_generators))

    result = []
    for matching_generator in matching_generators:
        for match in matching_generator.matches:
            generated_exercise = matching_generator.generator(sentence, match)

            if generated_exercise is not None:
                result.append(generated_exercise)

    return result

