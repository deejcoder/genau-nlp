from .fragment import Fragment
from .fragment_token import FragmentToken


class MultiChoiceFragment(Fragment):
    text: str = ""
    tokens: list[FragmentToken] = []
    options: list[list[FragmentToken]] = []
