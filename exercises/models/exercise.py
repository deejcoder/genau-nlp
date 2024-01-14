from abc import abstractmethod


class Exercise:
    def __init__(self, sentence: str):
        self.sentence = sentence

    @abstractmethod
    def format_for_logging(self):
        pass
