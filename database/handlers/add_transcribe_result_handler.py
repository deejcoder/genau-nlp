from database.models.transcribe_result import TranscribeResult
from database.commands.add_transcribe_result import AddTranscribeResultCommand
from database.models.transcribe_result_status import StatusEnum


async def add_transcribe_result_handler(command: AddTranscribeResultCommand):
    return await TranscribeResult.create(path=command.path, status=StatusEnum.pending.value)