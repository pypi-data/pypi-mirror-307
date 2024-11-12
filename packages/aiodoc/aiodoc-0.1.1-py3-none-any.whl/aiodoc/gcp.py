from io import BytesIO
from typing import List, Any, Union
from google.cloud import storage  # type: ignore
from aiodoc.base import BucketProvider


class GCPProvider(BucketProvider):
    def __init__(self, client: storage.Client) -> None:
        self.client: storage.Client = client

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        """
        Uploads a file to the specified bucket using the Google Cloud Storage client.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination)
        if isinstance(file, BytesIO):
            blob.upload_from_file(file, rewind=True)
        elif isinstance(file, str):
            blob.upload_from_filename(file)
        else:
            raise TypeError("Unsupported file type. Must be either 'str' or 'BytesIO'.")

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        """
        Downloads a file from the bucket using the Google Cloud Storage client and returns it as a BytesIO object.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        file = BytesIO()
        blob.download_to_file(file)
        file.seek(0)
        return file

    async def list_files(self, bucket_name: str) -> List[Any]:
        """
        Lists all files in the specified bucket using the Google Cloud Storage client.
        Returns a list of blob objects.
        """
        bucket = self.client.bucket(bucket_name)
        return list(bucket.list_blobs())

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        """
        Deletes the specified file from the bucket using the Google Cloud Storage client.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.delete()
