import os

from huggingface_hub import snapshot_download
from loguru import logger


def download_whisper_model(model_path: str):
    """
    下载 faster-whisper-large-v2 模型到指定路径

    Args:
        model_path (str): 模型保存的目标路径
    """
    try:
        # 确保目标目录存在
        os.makedirs(model_path, exist_ok=True)

        logger.info(f"开始下载模型到: {model_path}")

        # 使用 snapshot_download 下载模型
        snapshot_download(
            repo_id="guillaumekln/faster-whisper-large-v2",
            local_dir=model_path,
            local_dir_use_symlinks=False,
        )

        logger.success("模型下载完成")
        return True
    except Exception as e:
        logger.error(f"下载模型时出错: {str(e)}")
        return False
