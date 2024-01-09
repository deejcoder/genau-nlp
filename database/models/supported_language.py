from database.base import BaseEnumModel, DatabaseEnum, DatabaseEnumItem
from events.event import event, EventType


class SupportedLanguage(BaseEnumModel):

    class Index(DatabaseEnum):
        Deutsch = DatabaseEnumItem(1, 'deutsch', 'Deutsch')

    class Meta:
        table = "supported_language"


@event.on(EventType.Index.post_schema_generation)
async def __on_post_generate():
    await SupportedLanguage.insert_enum_values(SupportedLanguage.Index)
