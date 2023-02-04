from database.base import BaseEnumModel, DatabaseEnum, DatabaseEnumItem
from events import event, EventType


class JobType(BaseEnumModel):

    class Index(DatabaseEnum):
        transcribe = DatabaseEnumItem(1, "transcribe", "Transcribe")

    class Meta:
        table = "job_type"


@event.on(EventType.Index.post_schema_generation)
async def __on_post_generate():
    await JobType.insert_enum_values(JobType.Index)
