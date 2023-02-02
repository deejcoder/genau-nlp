from tortoise import fields, models

from database.bus import QueryBus
from database.queries.base import Query
from database.commands.base import Command
from typing import Type, TypeVar


T = TypeVar('T')


class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @classmethod
    def execute_query(cls, query: Query) -> Type[T]:
        return _bus.execute(query)

    @classmethod
    def execute_command(cls, command: Command):
        return _bus.execute(command)

    class Meta:
        abstract = True


_bus = QueryBus()
