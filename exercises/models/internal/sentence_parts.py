from spacy.tokens import Span


class SentenceParts:
    def __init__(self, start: Span, match: Span, end: Span):
        self.start = start
        self.match = match
        self.end = end
