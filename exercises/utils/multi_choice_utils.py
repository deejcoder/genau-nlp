from exercises.models.internal import SentenceParts
from exercises.models.public import MultiChoiceExercise, MultiChoiceFragment, FragmentToken
from spacy.tokens import Token


def compose_multi_choice_exercise(sentence_parts: SentenceParts, choices: list[list[Token]]):
    start = None

    if sentence_parts.start is not None:
        start = MultiChoiceFragment(tokens=[token_to_frag(token) for token in sentence_parts.start])
        start.text = sentence_parts.start.text

    choices = MultiChoiceFragment(
        tokens=[token_to_frag(token) for token in sentence_parts.match],
        options=[[token_to_frag(token) for token in choice] for choice in choices])
    choices.text = sentence_parts.match.text

    end = None
    if sentence_parts.end is not None:
        end = MultiChoiceFragment(tokens=[token_to_frag(token) for token in sentence_parts.end])
        end.text = sentence_parts.end.text

    fragments = []
    if start is not None:
        fragments.append(start)

    fragments.append(choices)

    if end is not None:
        fragments.append(end)

    return MultiChoiceExercise(fragments=fragments)


def token_to_frag(token: Token):
    return FragmentToken(
        text=token.text,
        is_punct=token.is_punct
    )
