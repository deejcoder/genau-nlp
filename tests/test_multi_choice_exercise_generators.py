import exercises.generators
from exercises import MultiChoiceExercise
from database.models import ExerciseGeneratorType

exercise_type = ExerciseGeneratorType.Index.MultiChoice
module = exercises.generators

by_pattern = exercises.get_exercise_generators_by_pattern(exercise_type, module, "Das ist ein großer Hund.")
# for this type of sentence, expect only the adjective declension generator
assert(len(by_pattern) == 1)

german_sentences = [
    "Im grünen Park spielt ein kleiner Hund.",
    "Im Frühling blüht der schöne Garten.",
    "Den aufmerksamen Leser fesselt die interessante Geschichte.",
    "Im schicken Laden hängt das elegante Kleid.",
    "In der geschäftigen Küche wird ein leckeres Essen zubereitet.",
    "Auf dem antiken Tisch liegt ein großes Buch.",
    "Nach einer warmen Decke verlangt der kalte Winterabend.",
    "In der belebten Straße befindet sich ein gemütliches Café.",
    "Im romantischen Garten duften die roten Rosen.",
    "Am ruhigen Fluss steht das alte Haus."
]

generated_exercises = []
for sentence in german_sentences:
    generated = exercises.generate_exercises(exercise_type, module, sentence)

    # we should have at least one exercise, but there could be more
    assert(len(generated) > 0)

    for ex in generated:
        assert(isinstance(ex, MultiChoiceExercise))
        print(ex.format_for_logging())

