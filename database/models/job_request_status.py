import enum
from database.models.base_enum import BaseEnumModel, DatabaseEnum, DatabaseEnumItem


class JobRequestStatus(BaseEnumModel):

    class Index(DatabaseEnum):
        pending = DatabaseEnumItem(1, 'pending', 'Pending')
        completed = DatabaseEnumItem(2, 'completed', 'Completed')
        failed = DatabaseEnumItem(3, 'failed', 'Failed')

    class Meta:
        table = "job_request_status"

    @classmethod
    async def on_post_generate(cls):
        await super().insert_enum_values(cls.Index)
        # values = [(s.value, s.name) for s in cls.Index]
        # for value in values:
        #     await cls.get_or_create(id=value[0], code=value[1])
