from io import BytesIO
from typing import List, Dict, Any, Union
from aiofile import async_open # type: ignore
from aiodoc.base import BucketProvider
from aiofiles.os import remove as async_remove

class FileProvider(BucketProvider):
    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        if isinstance(file, str):
            # If `file` is a file path, read the file as bytes
            async with async_open(file, 'rb') as f:
                content = await f.read()
        elif isinstance(file, BytesIO):
            file.seek(0)
            content = file.read()
        else:
            raise TypeError("The 'file' parameter must be either a string (file path) or BytesIO.")

        async with async_open(destination, 'wb') as f:
            await f.write(content)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        async with async_open(file_name, 'rb') as f:
            content = await f.read()
        return BytesIO(content)

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Listing files is not supported for File://")

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        await async_remove(file_name)
