from io import BytesIO
from typing import List, Dict, Any, Union
from aiobotocore.session import get_session  # type: ignore[import]
from aiodoc.base import BucketProvider

class S3Provider(BucketProvider):
    def __init__(self) -> None:
        self.session = get_session()

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        """
        Uploads a file to the specified bucket using the S3 client.
        """
        async with self.session.create_client('s3') as client:
            if isinstance(file, BytesIO):
                file.seek(0)  # Reset pointer to the beginning
                await client.put_object(Bucket=bucket_name, Key=destination, Body=file)
            elif isinstance(file, str):
                with open(file, 'rb') as f:
                    await client.put_object(Bucket=bucket_name, Key=destination, Body=f)

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        """
        Downloads a file from the bucket using the S3 client and returns it as a BytesIO object.
        """
        async with self.session.create_client('s3') as client:
            response: Dict[str, Any] = await client.get_object(Bucket=bucket_name, Key=file_name)
            file_data: bytes = await response['Body'].read()
            return BytesIO(file_data)

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        Lists all files in the specified bucket using the S3 client.
        Returns a list of dictionaries with file metadata.
        """
        async with self.session.create_client('s3') as client:
            response: Dict[str, Any] = await client.list_objects_v2(Bucket=bucket_name)
            return response.get('Contents', [])

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        """
        Deletes the specified file from the bucket using the S3 client.
        """
        async with self.session.create_client('s3') as client:
            await client.delete_object(Bucket=bucket_name, Key=file_name)
