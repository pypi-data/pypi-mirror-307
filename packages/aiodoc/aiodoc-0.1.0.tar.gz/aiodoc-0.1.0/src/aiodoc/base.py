from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from io import BytesIO

class BucketProvider(ABC):

    @abstractmethod
    async def upload(self, bucket_name: str, file: Union[str, BytesIO], destination: str) -> None:
        """
        Uploads a file to the specified bucket. The file can be a file path (str) or a BytesIO object.
        """
        pass

    @abstractmethod
    async def download(self, bucket_name: str, file_name: str) -> BytesIO:
        """
        Downloads a file from the bucket and returns it as a BytesIO object.
        """
        pass

    @abstractmethod
    async def list_files(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        Lists all files in the specified bucket. Returns a list of dictionaries with file details.
        """
        pass

    @abstractmethod
    async def delete_file(self, bucket_name: str, file_name: str) -> None:
        """
        Deletes the specified file from the bucket.
        """
        pass
