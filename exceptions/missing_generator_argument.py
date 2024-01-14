class MissingGeneratorArgument(Exception):
    def __init__(self, generator_name: str, argument: str, argument_type: str):
        self.generator_name = generator_name
        self.argument = argument
        self.argument_type = type
        super().__init__(f"The argument '{argument}' of type '{argument_type}' is missing from the generator '{generator_name}'")
