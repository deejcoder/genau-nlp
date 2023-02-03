from tortoise import fields
from database.models import BaseModel


class JobRequest(BaseModel):
    status = fields.IntField()
    path = fields.TextField()

    class Meta:
        table = "job_request"
