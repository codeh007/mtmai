import boto3
from google.genai import types  # noqa
from mtmai.core.config import settings


def upload_video(video_path: str, target_path: str):
    s3 = boto3.client(
        service_name="s3",
        endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
        aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
        aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
        region_name="auto",  # Must be one of: wnam, enam, weur, eeur, apac, auto
    )
    # 上传/更新文件
    with open(video_path, "rb") as f:
        s3.upload_fileobj(f, settings.CLOUDFLARE_R2_BUCKET, target_path)


def upload_file(file_path: str, target_path: str):
    s3 = boto3.client(
        service_name="s3",
        endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
        aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
        aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
        region_name="auto",  # Must be one of: wnam, enam, weur, eeur, apac, auto
    )
    # 上传/更新文件
    with open(file_path, "rb") as f:
        s3.upload_fileobj(f, settings.CLOUDFLARE_R2_BUCKET, target_path)
