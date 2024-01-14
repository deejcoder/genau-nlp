from .exercise import Exercise


class MultiChoiceExercise(Exercise):
    def __init__(self, sentence: str, answer: str, distractors: list[str]):
        super().__init__(sentence)
        self.answer = answer
        self.distractors = distractors

    def format_for_logging(self):
        return f"Sentence: {self.sentence}\r\nAnswer: {self.answer}\r\nDistractors: {self.distractors}"
