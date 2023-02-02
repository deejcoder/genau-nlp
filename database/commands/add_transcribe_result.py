from .base import Command


class AddTranscribeResultCommand(Command):
    def __init__(self, path: str):
        self.path = path

