import os.path
from pathlib import Path
from uuid import uuid4
import aiofiles

from fastapi import UploadFile
from database.models import TranscribeResult


class FileUploader:

    async def save_file(self, file: UploadFile, destination: Path) -> Path:
        try:

            if not destination.exists():
                # create the path if it doesn't exist
                destination.mkdir(parents=True)

            # generate a new file name using a random guid
            _, file_ext = os.path.splitext(file.filename)
            file_name = f"{str(uuid4())}{file_ext}"
            file_path = destination.joinpath(file_name)

            # does this file already exist? generate a new guid and try again
            # ... very unlikely
            if file_path.exists():
                return await self.save_file(file, destination)

            # asynchronously read and save the file
            async with aiofiles.open(str(file_path), mode='wb') as buffer:
                await buffer.write(await file.read())

            TranscribeResult.execute_query()

            return file_path

        finally:
            await file.close()


