import random
from typing import Optional

from spacy.tokens import Token, Span

from ..generation import exercise_generator
from exercises.models.public import MultiChoiceExercise
from database.models import ExerciseGeneratorType
from services import NlpBlob
from ..models.internal import SentenceParts
from exercises.utils import compose_multi_choice_exercise


g_id = "03d773f4-2372-4e5e-ac10-d927c685bef6"
pattern = [
    {'POS': 'DET'},
    {'POS': 'ADJ'},
    {'POS': 'NOUN'}
]


@exercise_generator(g_id, "Adjective declensions", ExerciseGeneratorType.Index.MultiChoice, pattern)
def generate(sentence: str, sentence_parts: SentenceParts) -> Optional[MultiChoiceExercise]:
    match = sentence_parts.match

    # given the pattern matches there will always be an adjective
    adj_token = find_adjective(match)
    rand_adj_declensions = get_random_adj_declensions(adj_token)

    choices = []

    # substitute the answer with each invalid declension to build a list of choices
    for adj_declension in rand_adj_declensions:
        choice_tokens = [token for token in match]
        adj_idx = choice_tokens.index(adj_token)
        choice_tokens[adj_idx] = adj_declension

        choices.append(choice_tokens)

    return compose_multi_choice_exercise(sentence_parts, choices)


def find_adjective(match: Span) -> Optional[Token]:
    for i in range(len(match)):
        if match[i].pos_ == "ADJ":
            return match[i]
    return None


def get_random_adj_declensions(adj_token: Token) -> list[Token]:
    lem = adj_token.lemma_

    # all possible adjective endings depending on their declension
    declensions = [
        lem + "er",
        lem + "e",
        lem + "es",
        lem + "en"
    ]

    valid_declensions = []
    for declension in declensions:
        token = NlpBlob(declension, "de").doc[0]
        if not token.is_oov:

            # do not include the original adjective
            if not token.text == adj_token.text:
                valid_declensions.append(token)

    if len(valid_declensions) == 0:
        return []

    # return a random three, there may be less
    num_items = min(3, len(valid_declensions))
    return random.sample(valid_declensions, num_items)
