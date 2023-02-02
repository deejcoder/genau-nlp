from typing import Type,  TypeVar


T = TypeVar('T')


class QueryBus:
    def __init__(self):
        self.handlers = {}

    def register(self, query, handler):
        self.handlers[query] = handler

    async def execute(self, query: Type[T]) -> T:
        if query in self.handlers:
            return await self.handlers[query](query)
        else:
            raise Exception(f"No handler registered for query: {query}")
