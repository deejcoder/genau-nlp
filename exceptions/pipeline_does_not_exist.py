class PipelineDoesNotExist(Exception):
    def __init__(self, lang: str):
        self.language = lang
        super().__init__(f"No pipeline exists for language '{lang}'")
