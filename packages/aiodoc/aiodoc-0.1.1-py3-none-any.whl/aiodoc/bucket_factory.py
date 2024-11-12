from aiodoc.base import BucketProvider
from typing import List, Dict, Any
from io import BytesIO

class BucketFactory:
    def __init__(self, provider: BucketProvider) -> None:
        self.provider: BucketProvider = provider

    async def upload(self, bucket_name: str, file_path: str, destination: str) -> None:
        """
        Uploads a file to the specified bucket using the provider.
        """
        return await self.provider.upload(bucket_name, file_path, destination)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        """
        Downloads a file from the bucket using the provider and returns it as a BytesIO object.
        """
        return await self.provider.download(bucket_name, file_name)

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        Lists all files in the specified bucket using the provider.
        """
        return await self.provider.list_files(bucket_name)

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        """
        Deletes the specified file from the bucket using the provider.
        """
        return await self.provider.delete_file(bucket_name, file_name)
