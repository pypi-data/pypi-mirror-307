from io import BytesIO
from typing import List, Dict, Any, Union
from aiomemcached import Client as MemcachedClient # type: ignore
from aiodoc.base import BucketProvider


class MemcachedProvider(BucketProvider):
    def __init__(self, client: MemcachedClient):
        self.client = client

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        # Handle both string and BytesIO inputs to ensure compatibility with the base class definition
        if isinstance(file, BytesIO):
            file.seek(0)
            content = file.read()
        elif isinstance(file, str):
            content = file.encode('utf-8')
        else:
            raise TypeError("Invalid file type. Expected str or BytesIO.")

        await self.client.set(destination, content)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        content = await self.client.get(file_name)
        return BytesIO(content) if content else BytesIO()

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Listing files is not supported for Memcached")

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        await self.client.delete(file_name)
