from io import BytesIO
from typing import List, Dict, Any, Union
from httpx import AsyncClient # type: ignore
from aiodoc.base import BucketProvider

# HTTP Provider
class HTTPProvider(BucketProvider):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        if isinstance(file, str):
            # Assuming the file parameter is a file path, open it as a BytesIO
            with open(file, 'rb') as f:
                content = f.read()
        elif isinstance(file, BytesIO):
            file.seek(0)
            content = file.read()
        else:
            raise TypeError("The 'file' parameter must be either a string (file path) or BytesIO.")

        await self.client.post(destination, content=content)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        response = await self.client.get(file_name)
        response.raise_for_status()  # Ensure successful request
        return BytesIO(response.content)

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Listing files is not supported for HTTP")

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        response = await self.client.delete(file_name)
        response.raise_for_status()  # Ensure successful request
