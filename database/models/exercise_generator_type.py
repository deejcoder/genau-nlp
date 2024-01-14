from database.base import BaseEnumModel, DatabaseEnum, DatabaseEnumItem
from events.event import event, EventType


class ExerciseGeneratorType(BaseEnumModel):

    class Index(DatabaseEnum):
        MultiChoice = DatabaseEnumItem(1, 'multi_choice', 'Multi Choice')

    class Meta:
        table = "exercise_generator_type"


@event.on(EventType.Index.post_schema_generation)
async def __on_post_generate():
    await ExerciseGeneratorType.insert_enum_values(ExerciseGeneratorType.Index)
