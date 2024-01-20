from exercises.models.internal import SentenceParts
from exercises.models.public import MultiChoiceExercise, MultiChoiceFragment, FragmentToken, MultiChoiceOption
from spacy.tokens import Token
from nlp import NlpToolkit


def map_from_internal(sentence_parts: SentenceParts, choices: list[list[Token]]):
    start = None

    if sentence_parts.start is not None:
        start = MultiChoiceFragment(tokens=[token_to_frag(token) for token in sentence_parts.start])
        start.text = sentence_parts.start.text

    options = []
    for choice in choices:
        choice_text = NlpToolkit.detokenize(choice)
        fragment_tokens = [token_to_frag(token) for token in choice]
        option = MultiChoiceOption(text=choice_text, tokens=fragment_tokens)
        options.append(option)

    exercise_fragment = MultiChoiceFragment(
        tokens=[token_to_frag(token) for token in sentence_parts.match],
        options=options)
    exercise_fragment.text = sentence_parts.match.text

    end = None
    if sentence_parts.end is not None:
        end = MultiChoiceFragment(tokens=[token_to_frag(token) for token in sentence_parts.end])
        end.text = sentence_parts.end.text

    fragments = []
    if start is not None:
        fragments.append(start)

    fragments.append(exercise_fragment)

    if end is not None:
        fragments.append(end)

    return MultiChoiceExercise(fragments=fragments)


def token_to_frag(token: Token):
    return FragmentToken(
        text=token.text,
        isPunct=token.is_punct
    )
