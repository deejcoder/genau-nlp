import random
from typing import List, Optional

from spacy.tokens import Token

import exercises
from exercises import exercise_generator
from database.models import ExerciseGeneratorType
from exercises import MultiChoiceExercise
from services import NlpBlob

pattern = "DET ADJ NOUN"


@exercise_generator(ExerciseGeneratorType.Index.MultiChoice, pattern)
def generate(sentence: str, matching_tokens: List[Token]) -> Optional[MultiChoiceExercise]:
    # given the pattern matches there will always be an adjective
    adj_token = find_adjective(matching_tokens)
    rand_adj_declensions = get_random_adj_declensions(adj_token)

    answer = " ".join([token.text for token in matching_tokens])
    distractors = []

    # put the invalid declensions in the original matched pattern as destractors
    for adj_declension in rand_adj_declensions:
        values = [token.text for token in matching_tokens]
        adj_idx = values.index(adj_token.text)
        values[adj_idx] = adj_declension

        distractor = " ".join(values)
        distractors.append(distractor)

    return MultiChoiceExercise(
        sentence=sentence,
        answer=answer,
        distractors=distractors
    )


def find_adjective(tokens: List[Token]) -> Optional[Token]:
    for i in range(len(tokens)):
        if tokens[i].pos_ == "ADJ":
            return tokens[i]
    return None


def get_random_adj_declensions(adj_token: Token):
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
            valid_declensions.append(token.text)

    if len(valid_declensions) == 0:
        return []

    # remove the original adjective if it exists
    if adj_token.text in valid_declensions:
        valid_declensions.remove(adj_token.text)

    # return a random three, there may be less
    num_items = min(3, len(valid_declensions))
    return random.sample(valid_declensions, num_items)
