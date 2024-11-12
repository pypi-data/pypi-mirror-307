from minio import Minio # type: ignore
from io import BytesIO
from typing import Union, List, Dict, Any
from aiodoc.base import BucketProvider 
import asyncio
from concurrent.futures import ThreadPoolExecutor

class MinioProvider(BucketProvider):
    def __init__(self, client: Minio) -> None:
        self.client: Minio = client
        self.executor = ThreadPoolExecutor()

    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        """
        Uploads a file to the specified bucket using the Minio client.
        """
        if isinstance(file, str):
            # If file is a string, it is treated as a file path.
            def upload_from_file():
                with open(file, 'rb') as f:
                    self.client.put_object(bucket_name, destination, f, length=-1, part_size=10 * 1024 * 1024)

            await asyncio.get_running_loop().run_in_executor(self.executor, upload_from_file)
        
        elif isinstance(file, BytesIO):
            file.seek(0)
            await asyncio.get_running_loop().run_in_executor(
                self.executor,
                lambda: self.client.put_object(bucket_name, destination, file, length=len(file.getvalue()))
            )
        else:
            raise ValueError("file must be either a str or a BytesIO object")

    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        """
        Downloads a file from the bucket using the Minio client and returns it as a BytesIO object.
        """
        def get_object():
            response = self.client.get_object(bucket_name, file_name)
            content = response.read()
            response.close()
            response.release_conn()
            return content

        content = await asyncio.get_running_loop().run_in_executor(self.executor, get_object)
        return BytesIO(content)

    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        Lists all files in the specified bucket using the Minio client.
        """
        objects = await asyncio.get_running_loop().run_in_executor(
            self.executor,
            lambda: list(self.client.list_objects(bucket_name))
        )
        return [{"object_name": obj.object_name, "size": obj.size} for obj in objects]

    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        """
        Deletes the specified file from the bucket using the Minio client.
        """
        await asyncio.get_running_loop().run_in_executor(
            self.executor,
            lambda: self.client.remove_object(bucket_name, file_name)
        )
