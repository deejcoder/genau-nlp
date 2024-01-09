from tortoise import fields, models
from collections import namedtuple
from typing import Type, Optional
import enum


DatabaseEnumItem = namedtuple('DescriptiveEnumItem', ['value', 'code', 'description'])


class DatabaseEnum(DatabaseEnumItem, enum.Enum):
    pass


class BaseEnumModel(models.Model):
    id = fields.IntField(pk=True)
    code = fields.TextField(max_length=50, required=True)
    description = fields.TextField(max_length=100, required=True)

    class Meta:
        abstract = True

    @classmethod
    async def insert_enum_values(cls, db_enum: Type[DatabaseEnum]):
        for db_enum_item in db_enum:
            await cls.get_or_create(id=db_enum_item.value, code=db_enum_item.code, description=db_enum_item.description)

    @classmethod
    def get_value_from_code(cls, code: str, db_enum: Type[DatabaseEnum]):
        for db_enum_item in db_enum:
            if db_enum_item.code is code:
                return db_enum_item.value
        return None
