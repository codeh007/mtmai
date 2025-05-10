import boto3
from google.genai import types  # noqa

from mtmai.core.config import settings


class Mtfs:
    """
    文件上传工具类
    """

    def get_Client(self):
        """
        获取 S3 客户端
        """
        s3_client = boto3.client(
            service_name="s3",
            endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
            region_name="auto",  # Must be one of: wnam, enam, weur, eeur, apac, auto
        )
        return s3_client

    async def upload_file(
        self,
        file_path: str | bytes,
        target_path: str,
        content_type: str = "application/json",
    ):
        if isinstance(file_path, str):
            with open(file_path, "rb") as f:
                self.get_Client().upload_fileobj(
                    f,
                    settings.CLOUDFLARE_R2_BUCKET,
                    target_path,
                    ExtraArgs={"ContentType": content_type},
                )
        else:
            self.get_Client().put_object(
                Body=file_path,
                Bucket=settings.CLOUDFLARE_R2_BUCKET,
                Key=target_path,
                ContentType=content_type,
            )

    async def put_object(
        self,
        Body: bytes,
        Key: str,
        ContentType: str = "application/json",
    ):
        self.get_Client().put_object(
            Body=Body,
            # Bucket=Bucket,
            Bucket=settings.CLOUDFLARE_R2_BUCKET,
            Key=Key,
            ContentType=ContentType,
        )


mts3fs = None


def get_s3fs():
    global mts3fs
    if mts3fs is None:
        mts3fs = Mtfs()
    return mts3fs
