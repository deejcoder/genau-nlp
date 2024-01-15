import inspect
import types
import random
import typing
from functools import wraps

from spacy.tokens import Token

from exceptions import MissingGeneratorArgument
from typing import Tuple, List, Callable, get_type_hints
from services import NlpBlob
from database.models import ExerciseGeneratorType
from .models.exercise import Exercise
from .models.multi_choice_exercise import MultiChoiceExercise

cached_generators: List[Callable] = []


def exercise_generator(exercise_type: ExerciseGeneratorType.Index, sentence_pattern: str) -> Callable:
    """
    A decorator used to indicate exercise generators
    :param exercise_type: the type of exercise the generator belongs to
    :param sentence_pattern: a pattern containing deps that the input sentence must statify
        for the generator to be valid
    :return: Callable
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            expected_param = "sentence"
            expected_param_type = str

            hints = get_type_hints(func)
            has_expected_param = False
            for param, hint in hints.items():
                if param is expected_param and expected_param_type is hint:
                    has_expected_param = True

            if not has_expected_param:
                raise MissingGeneratorArgument(func.__name__, expected_param, expected_param_type.__name__)

            if 'return' in hints:
                return_type_hint = hints['return']
                if not issubclass(return_type_hint, typing.Optional[Exercise]):
                    raise ValueError(
                        f"The generator '{func.__name__}' must return a model that inherits from '{Exercise.__name__}'")

            return func(*args, **kwargs)

        setattr(wrapper, '_is_exercise_generator', True)
        setattr(wrapper, '_exercise_type', exercise_type)
        setattr(wrapper, '_sentence_pattern', sentence_pattern)
        return wrapper

    return decorator


def get_exercise_generators(module: types.ModuleType) -> List[Callable]:
    """
    Returns a list of exercise generators
    :param module: the module where the generators are located
    :return:
    """
    if len(cached_generators) != 0:
        return cached_generators

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and hasattr(obj, '_is_exercise_generator'):
            cached_generators.append(obj)

    return cached_generators


def get_exercise_generators_by_pattern(exercise_type: ExerciseGeneratorType.Index, module: types.ModuleType,
                                       sentence: str) -> List[Tuple[Callable, List[Token]]]:
    """
    Compares each exercise generator based on its pattern, with the input sentence
    :param exercise_type the type of exercise
    :param module: the module where the generators are located
    :param sentence:
    :return: a list of matching callable generators
    """
    matching_generators = []

    for generator in get_exercise_generators(module):
        if exercise_type != getattr(generator, '_exercise_type'):
            continue

        pattern = getattr(generator, '_sentence_pattern')

        for matches in get_pattern_occurrences(sentence, pattern):
            matching_generators.append((generator, matches))

    return matching_generators


def get_pattern_occurrences(sentence: str, pattern: str) -> List[List[Token]]:
    """
    Checks if the input sentence matches the pattern
    :param sentence:
    :param pattern: a string for the expected sentence structure
    :return: true or false
    """
    pattern_tags = pattern.split(' ')

    matches = get_tokens_from_pattern(sentence, pattern)
    pattern_occurrences = []
    for i in range(len(matches) // len(pattern_tags)):
        lower_idx = (i * len(pattern_tags))
        upper_idx = lower_idx + len(pattern_tags)
        pattern_occurrences.append(matches[lower_idx:upper_idx])

    return pattern_occurrences


def get_tokens_from_pattern(sentence: str, pattern: str) -> List[Token]:
    matching_tokens = []

    # get dep tags from the input sentence
    sentence_blob = NlpBlob(sentence, "de")

    # split the pattern by spaces to get a list of tags we need to compare
    pattern_tags = pattern.split(' ')

    doc = sentence_blob.doc

    for i in range(len(doc) - len(pattern_tags) + 1):
        is_pattern_matched = all(_compare_token(doc[i + j], pattern_tags[j]) for j in range(len(pattern_tags)))

        if is_pattern_matched:
            matching_tokens.extend(doc[i:i + len(pattern_tags)])

    return matching_tokens


def _compare_token(token: Token, expected_tag):
    # * means any word in this slot is valid
    # if expected_tag == "*":
    #    return True

    if expected_tag == token.pos_:
        return True

    if expected_tag == token.dep_:
        return True

    if expected_tag in token.morph:
        return True

    return False


def generate_exercises(exercise_type: ExerciseGeneratorType.Index,
                       module: types.ModuleType,
                       sentence: str) -> List[Exercise]:
    """
    Generates a random exercise based on the available exercise generators
    :param exercise_type: the abstract type of exercise to generate
    :param module: where to look for exercise generators
    :param sentence: the sentence to base the exercise on
    :return: a generated exercise
    """
    generators = get_exercise_generators_by_pattern(exercise_type, module, sentence)

    if len(generators) == 0:
        return []

    result = []
    for generator in generators:
        ex = generator[0](sentence, generator[-1])
        if ex is not None:
            result.append(ex)
    return result
