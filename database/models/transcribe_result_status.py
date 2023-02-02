import enum
from tortoise import fields

from database.models import BaseModel


class StatusEnum(enum.Enum):
    pending = 1
    completed = 2
    failed = 3


class TranscribeResultStatus(BaseModel):
    code = fields.TextField(max_length=100, required=True)

    class Meta:
        table = "transcribe_result_status"

    @classmethod
    async def on_post_generate(cls):
        values = [(s.value, s.name) for s in StatusEnum]
        for value in values:
            await TranscribeResultStatus.get_or_create(id=value[0], code=value[1])
