from tortoise import fields
from database.models import BaseModel


class TranscribeResult(BaseModel):
    status = fields.IntField()
    path = fields.TextField()

    class Meta:
        table = "transcribe_result"
