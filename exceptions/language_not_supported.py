class LanguageNotSupported(Exception):
    def __init__(self, language: str):
        self.language = language
        super().__init__(f'Language \'{self.language}\' is not supported')
