from io import BytesIO
from typing import Union, List, Dict, Any
from aiodoc.base import BucketProvider
from redis.asyncio import Redis

class RedisProvider(BucketProvider):
    def __init__(self, client: Redis):
        self.client = client

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        if isinstance(file, str):
            # If file is a string, assume it is a path, and read its content
            with open(file, 'rb') as f:
                content = f.read()
        elif isinstance(file, BytesIO):
            # If file is a BytesIO object, get its content
            file.seek(0)
            content = file.read()
        else:
            raise ValueError("file must be either a str or a BytesIO object")

        await self.client.set(destination, content)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        content = await self.client.get(file_name)
        return BytesIO(content) if content else BytesIO()

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Listing files is not supported for Redis")

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        await self.client.delete(file_name)
