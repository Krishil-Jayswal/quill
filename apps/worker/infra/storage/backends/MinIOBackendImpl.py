import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from pathlib import Path
from config import settings
from ..base import StorageBackend

class MinIOStorageBackendImpl(StorageBackend):
    def __init__(self) -> None:
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name=settings.MINIO_REGION,
            use_ssl=settings.MINIO_SECURE,
            config=Config(
                signature_version="s3v4",
            ),
        )

        self._bucket = settings.MINIO_BUCKET

    def upload_file(self, local_path: str, object_key: str) -> None:
        self._client.upload_file(
            local_path,
            self._bucket,
            object_key,
        )

    def upload_directory(self, local_dir: str, object_prefix: str) -> None:
        directory = Path(local_dir)

        if not directory.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {local_dir}"
            )

        for file_path in directory.rglob("*"):
            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(directory)

            object_key = (
                f"{object_prefix.rstrip("/")}/"
                f"{relative_path.as_posix()}"
            )

            self.upload_file(
                local_path=str(file_path),
                object_key=object_key
            )

    def download_file(self, object_key: str, local_path: str) -> None:
        destination = Path(local_path)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._client.download_file(
            self._bucket,
            object_key,
            str(destination),
        )

    def download_files(self, object_keys: list[str], local_dir: str) -> None:
        directory = Path(local_dir)

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        for object_key in object_keys:
            filename = Path(object_key).name
            local_path = directory / filename

            self.download_file(
                object_key=object_key,
                local_path=str(local_path)
            )
    
    def download_folder(self, object_prefix: str, local_path: str):
        destination = Path(local_path)

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        paginator = self._client.get_paginator("list_objects_v2")

        for page in paginator.paginate(
            Bucket=self._bucket,
            Prefix=object_prefix.rstrip("/") + "/",
        ):
            for obj in page.get("Contents", []):
                object_key = obj["Key"]

                relative_path = Path(object_key).relative_to(object_prefix.rstrip("/"))

                local_file = destination / relative_path

                self.download_file(
                    object_key=object_key,
                    local_path=str(local_file)
                )


    def exists(self, object_key: str) -> bool:
        try:
            self._client.head_object(
                Bucket=self._bucket,
                Key=object_key,
            )

            return True
        except ClientError as error:
            error_code = error.response.get(
                "Error",
                {},
            ).get("Code")

            if error_code in ["404", "NoSuchKey", "NotFound"]:
                return False

            raise

    def delete(self, object_key: str) -> None:
        self._client.delete_object(
            Bucket=self._bucket,
            Key=object_key
        )