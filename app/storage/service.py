import uuid
from pathlib import Path
from uuid import UUID

from app.models.enums import MediaType

from fastapi import UploadFile
from minio.error import S3Error

from app.core.config import settings
from app.storage.client import minio_client

class StorageService:
    def __init__(self):
        self.client = minio_client

    def ensure_bucket_exists(self) -> None:
        try:
            if not self.client.bucket_exists(settings.minio_bucket):
                self.client.make_bucket(settings.minio_bucket)
                print(f"Bucket '{settings.minio_bucket}' created successfully.")
            else:
                print(f"Bucket '{settings.minio_bucket}' already exists.")

        except S3Error as e:
            raise RuntimeError(f"Failed to initialize bucket: {e}")

    async def upload_file(
        self,
        file: UploadFile,
        user_id: UUID,
        media_type: MediaType,
    ) -> str:
        try:
            extension = Path(file.filename).suffix

            object_name = (
                f"users/{user_id}/{media_type}/"
                f"{uuid.uuid4()}{extension}"
            )

            file.file.seek(0)

            self.client.put_object(
                bucket_name=settings.minio_bucket,
                object_name=object_name,
                data=file.file,
                length=file.size,
                content_type=file.content_type,
            )

            return object_name

        except S3Error as e:
            raise RuntimeError(f"Failed to upload file: {e}")

    def download_file(self, object_name: str):
        try:
            return self.client.get_object(
                bucket_name=settings.minio_bucket,
                object_name=object_name,
            )

        except S3Error as e:
            raise RuntimeError(f"Failed to download file: {e}")

    def delete_file(self, object_name: str) -> None:
        try:
            self.client.remove_object(
                bucket_name=settings.minio_bucket,
                object_name=object_name,
            )
        except S3Error as e:
            if e.code != "NoSuchKey":
                raise RuntimeError(f"Failed to delete file: {e}")

    def generate_presigned_url(
        self,
        object_name: str,
        expires: int = 3600,
    ) -> str:
        try:
            from datetime import timedelta

            return self.client.presigned_get_object(
                bucket_name=settings.minio_bucket,
                object_name=object_name,
                expires=timedelta(seconds=expires),
            )

        except S3Error as e:
            raise RuntimeError(f"Failed to generate presigned URL: {e}")