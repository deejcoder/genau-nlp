from ..models import MultiChoiceExercise
from ..generation import exercise_generator, ExerciseGeneratorType
from typing import Optional
from spacy.tokens import Token, Span
from pattern.text.de import article, DEFINITE, INDEFINITE, FEMALE, MALE, NEUTER, \
    ACCUSATIVE, DATIVE, NOMINATIVE
import random
from exercises.models.internal import SentenceParts
from exercises.utils import compose_multi_choice_exercise
from services.nlp import NlpBlob


g_id = "8187c404-e6fa-46f1-833c-d13ecda83b00"
pattern = [
    {'POS': 'DET'},
    {'POS': 'NOUN'}
]


@exercise_generator(g_id, "Genders of nouns", ExerciseGeneratorType.Index.MultiChoice, pattern)
def generate(sentence: str, sentence_parts: SentenceParts) -> Optional[MultiChoiceExercise]:
    match = sentence_parts.match
    det = find_by_token_pos(match, "DET")
    noun = find_by_token_pos(match, "NOUN")

    valid_cases = [
        NOMINATIVE,
        ACCUSATIVE,
        DATIVE,
    ]

    morph = noun.morph.to_dict()

    if morph['Number'] == "Plur":
        return None

    match morph['Case']:
        case "Acc":
            valid_cases.remove(ACCUSATIVE)
        case "Dat":
            valid_cases.remove(DATIVE)
        case "Nom":
            valid_cases.remove(NOMINATIVE)

    possible_articles = []

    for case in valid_cases:
        possible_articles.append(article(noun, DEFINITE, gender=FEMALE, role=case))
        possible_articles.append(article(noun, DEFINITE, gender=MALE, role=case))
        possible_articles.append(article(noun, DEFINITE, gender=NEUTER, role=case))
        possible_articles.append(article(noun, INDEFINITE, gender=FEMALE, role=case))
        possible_articles.append(article(noun, INDEFINITE, gender=MALE, role=case))
        possible_articles.append(article(noun, INDEFINITE, gender=NEUTER, role=case))

    rand_articles = random.sample(set(possible_articles), 3)

    choices = []

    for rand_article in rand_articles:
        choice_tokens = [token for token in match]
        det_idx = choice_tokens.index(det)
        choice_tokens[det_idx] = NlpBlob(rand_article, "de").doc[0]

        choices.append(choice_tokens)

    return compose_multi_choice_exercise(sentence_parts=sentence_parts, choices=choices)


def find_by_token_pos(span: Span, pos: str) -> Optional[Token]:
    for i in range(len(span)):
        if span[i].pos_ == pos:
            return span[i]
    return None



