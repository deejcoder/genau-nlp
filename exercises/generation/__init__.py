import inspect
import types
from functools import wraps
from typing import Callable, List, get_type_hints

import typing

from spacy.matcher import Matcher
from spacy.tokens import Span

from database.models import ExerciseGeneratorType, SupportedLanguage
from exceptions import MissingGeneratorArgument
from services import NlpBlob
from services.nlp import ModelLoader
from exercises.models import Exercise, MatchingGenerator, Generator

cached_generators: List[Generator] = []


def exercise_generator(
        g_id: str,
        description: str,
        exercise_type: ExerciseGeneratorType.Index,
        pattern: list[dict[str, typing.Any]]) -> Callable:
    """
    A decorator used to indicate exercise generators
    :param g_id: a guid that uniquely identifies the generator
    :param description: the description of the generator
    :param exercise_type: the type of exercise the generator belongs to
    :param pattern: a pattern containing deps that the input sentence must statify
        for the generator to be valid
    :return: Callable
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # expect at least one param for the input sentence
            expected_param = "sentence"
            expected_param_type = str

            hints = get_type_hints(func)
            has_expected_param = False
            for param, hint in hints.items():
                if param is expected_param and expected_param_type is hint:
                    has_expected_param = True

            if not has_expected_param:
                raise MissingGeneratorArgument(func.__name__, expected_param, expected_param_type.__name__)

            # check the return type is valid
            if 'return' in hints:
                return_type_hint = hints['return']

                if typing.get_origin(return_type_hint) is typing.Union:
                    inner_return_types = typing.get_args(return_type_hint)

                    # 2 := Exercise | None
                    if len(inner_return_types) != 2 or not issubclass(inner_return_types[0], Exercise):
                        raise ValueError(
                            f"The generator '{func.__name__}' must return a model that inherits from '{Exercise.__name__}'")

            return func(*args, **kwargs)

        setattr(wrapper, '_is_exercise_generator', True)
        setattr(wrapper, '_generator_id', g_id)
        setattr(wrapper, '_generator_description', description)
        setattr(wrapper, '_exercise_type', exercise_type)
        setattr(wrapper, '_pattern', pattern)
        return wrapper

    return decorator


def get_exercise_generators(module: types.ModuleType) -> List[Generator]:
    """
    Returns a list of exercise generators
    :param module: the module where the generators are located
    :return:
    """
    if len(cached_generators) != 0:
        return cached_generators

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and hasattr(obj, '_is_exercise_generator'):
            g_id = getattr(obj, "_generator_id")
            description = getattr(obj, "_generator_description")
            exercise_type = getattr(obj, "_exercise_type")
            pattern = getattr(obj, "_pattern")
            path = module.__name__ + "." + name
            cached_generators.append(Generator(g_id, obj, path, description, exercise_type, pattern))

    return cached_generators


def get_exercise_generators_by_pattern(exercise_type: ExerciseGeneratorType.Index, module: types.ModuleType,
                                       sentence: str) -> List[MatchingGenerator]:
    """
    Compares each exercise generator based on its pattern, with the input sentence
    :param exercise_type the type of exercise
    :param module: the module where the generators are located
    :param sentence:
    :return: a list of matching generators
    """
    matching_generators = []

    for generator in get_exercise_generators(module):
        if exercise_type != generator.exercise_type:
            continue

        matches = compare_generator_pattern(sentence, generator.pattern)
        if len(matches) > 0:
            matching_generators.append(MatchingGenerator(generator.g_id, generator.func, generator.path, matches))

    return matching_generators


def compare_generator_pattern(sentence: str, pattern: list[dict[str, typing.Any]]) -> List[Span]:
    """
    Checks if the pattern of a generator matches the input sentence
    :param sentence:
    :param pattern:
    :return: a list of matches
    """
    sentence_blob = NlpBlob(sentence, "de")

    model = ModelLoader.load(SupportedLanguage.Index.Deutsch)
    matcher = Matcher(model.vocab)
    matcher.add("pattern", [pattern])
    matches = matcher(sentence_blob.doc)

    result = []
    for match_id, start, end in matches:
        result.append(Span(sentence_blob.doc, start, end))

    return result

