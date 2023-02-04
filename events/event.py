import enum
from typing import Any

from pymitter import EventEmitter


class EventType:
    class Index(str, enum.Enum):
        @staticmethod
        def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
            return name.lower()

        post_schema_generation = enum.auto


class EventManager(EventEmitter):
    pass


event: EventManager = EventManager()
