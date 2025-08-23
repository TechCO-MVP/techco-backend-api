import boto3
import json

from src.repositories.repository import IStorageRepository
from typing import TypeVar

T = TypeVar("T")


class S3StorageRepository(IStorageRepository[dict]):
    def __init__(self, bucket_name: str):
        super().__init__()
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def get(self, key: str, format="") -> dict:
        try:
            file = self.get_file(key, format)
            data = file.decode("utf-8")
            return json.loads(data)
        except self.s3_client.exceptions.NoSuchKey:
            raise KeyError(f"Key {key} not found in bucket {self.bucket_name}")

    def put(self, key: str, value: dict):
        try:
            data = json.dumps(value)
            self.s3_client.put_object(Bucket=self.bucket_name, Key=f"{key}.json", Body=data)
        except Exception as e:
            raise RuntimeError(f"Failed to put object {key} in bucket {self.bucket_name}: {e}")

    def put_raw(self, key: str, value: bytes, content_type: str):
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name, Key=key, Body=value, ContentType=content_type
            )
        except Exception as e:
            raise RuntimeError(f"Failed to put object {key} in bucket {self.bucket_name}: {e}")

    def delete(self, key: str):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except Exception as e:
            raise RuntimeError(f"Failed to delete object {key} from bucket {self.bucket_name}: {e}")

    def get_file(self, key: str, format: str = "") -> bytes:
        try:
            name = f"{key}.{format}" if format else key
            print(name)
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=name)
            return response["Body"].read()
        except self.s3_client.exceptions.NoSuchKey:
            raise KeyError(f"Key {name} not found in bucket {self.bucket_name}")
