from .fragment import Fragment
from .fragment_token import FragmentToken
from .multi_choice_option import MultiChoiceOption


class MultiChoiceFragment(Fragment):
    text: str = ""
    tokens: list[FragmentToken] = []
    options: list[MultiChoiceOption] = []
