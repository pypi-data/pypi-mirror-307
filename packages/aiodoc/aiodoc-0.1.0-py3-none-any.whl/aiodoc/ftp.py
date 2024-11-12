from io import BytesIO
from typing import List, Dict, Any, Union
from aioftp import Client as FtpClient  # type: ignore[import]
from aiodoc.base import BucketProvider

class FTPProvider(BucketProvider):
    def __init__(self, client: FtpClient):
        self.client = client

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        if isinstance(file, BytesIO):
            file.seek(0)
        await self.client.upload_stream(file, destination)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        file = BytesIO()
        await self.client.download_stream(file_name, file)
        file.seek(0)
        return file

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        files = []
        async for path in self.client.list(bucket_name):
            files.append(dict(path))
        return files

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        await self.client.remove(file_name)
