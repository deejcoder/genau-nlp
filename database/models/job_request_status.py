from database.base import BaseEnumModel, DatabaseEnum, DatabaseEnumItem
from events.event import event, EventType


class JobRequestStatus(BaseEnumModel):

    class Index(DatabaseEnum):
        pending = DatabaseEnumItem(1, 'pending', 'Pending')
        completed = DatabaseEnumItem(2, 'completed', 'Completed')
        failed = DatabaseEnumItem(3, 'failed', 'Failed')

    class Meta:
        table = "job_request_status"


@event.on(EventType.Index.post_schema_generation)
async def __on_post_generate():
    await JobRequestStatus.insert_enum_values(JobRequestStatus.Index)
