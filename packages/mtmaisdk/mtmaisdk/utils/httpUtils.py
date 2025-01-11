from pathlib import Path

import httpx


# def download_file(url: str, dest: Path):
#     response = httpx.get(url, stream=True)
#     response.raise_for_status()
#     dest.parent.mkdir(parents=True, exist_ok=True)
#     with Path.open(dest, "wb") as f:
#         for chunk in response.iter_content(chunk_size=8192):
#             f.write(chunk)
#     dest.chmod(0o755)
async def download_file(url: str, dest: str | Path):
    dest = Path(dest)
    with httpx.Client(follow_redirects=True) as client:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        # dest.chmod(0o755)



def download_file_to_dir(url: str, dest: Path):
    """
    下载文件到指定目录, 文件名使用 url 对应的文件名
    """
    # 提取文件名并拼接到目标路径
    filename = url.split("/")[-1]
    dest_file = dest / filename

    # 创建目标文件的父目录
    dest_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with httpx.stream("GET", url) as response:
            response.raise_for_status()
            with dest_file.open("wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        # 设置文件权限
        dest_file.chmod(0o755)

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
