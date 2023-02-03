import enum
from tortoise import fields

from database.models.base_enum import BaseEnumModel, DatabaseEnum, DatabaseEnumItem


class JobType(BaseEnumModel):

    class Index(DatabaseEnum):
        transcribe = DatabaseEnumItem(1, "transcribe", "Transcribe")

    class Meta:
        table = "job_type"

    @classmethod
    async def on_post_generate(cls):
        await super().insert_enum_values(cls.Index)

