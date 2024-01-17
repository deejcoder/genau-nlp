from .multi_choice_fragment import MultiChoiceFragment
from .exercise import Exercise


class MultiChoiceExercise(Exercise):
    fragments: list[MultiChoiceFragment] = []
