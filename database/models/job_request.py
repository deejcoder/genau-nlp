from tortoise import fields
from database.base import BaseModel


class JobRequest(BaseModel):
    status = fields.IntField()
    path = fields.TextField()

    class Meta:
        table = "job_request"
