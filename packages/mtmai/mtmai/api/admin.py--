import logging
import os
import shutil
import threading
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from mtmai.core.config import settings
from mtmai.deps import CurrentUser, get_current_active_superuser
from mtmlib.mtutils import bash

router = APIRouter()

logger = logging.getLogger()


# @router.get(
#     "/dp",
#     dependencies=[Depends(get_current_active_superuser)],
#     status_code=201,
# )
# def dp():
#     bash(
#         "cd mtmai && poetry export --format requirements.txt --output requirements.txt --without-hashes --without dev"
#     )
#     vercel_token = settings.vercel_token

#     if not vercel_token:
#         msg = "require vercel token"
#         raise Exception(msg)
#     bash(f"""poetry run poe test && \
#         vercel link --project=mtmai --yes --token="{vercel_token}" && \
#         vercel deploy --yes --local-config vercel.json --prod --token="{vercel_token}"
#     """)


@router.get(
    "/build_docker",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def build_docker(
    user: CurrentUser,  # noqa: ARG001
):
    bash("docker build --progress=plain -t gitgit188/mtmai .")
    bash("docker push gitgit188/mtmai")

    return ""


@router.get(
    "/testing_fs", dependencies=[Depends(get_current_active_superuser)], status_code=201
)
async def testing_fs():
    dir_base = settings.STORAGE_DIR_BASE
    target_file = Path(dir_base) / "hello.txt"
    Path(target_file).write_text("hello2")
    content = Path(target_file).read_text()
    return content


@router.get(
    "/envs", dependencies=[Depends(get_current_active_superuser)], status_code=201
)
async def envs(
    user: CurrentUser,
):
    import grp
    import pwd

    try:
        # Get the home directory
        user_home_dir = str(Path.home())

        uid = os.getuid()
        gid = os.getgid()
        user_info = pwd.getpwuid(uid)
        group_info = grp.getgrgid(gid)
    except Exception as e:
        return {"error": f"Error retrieving user info: {e!s}"}

    try:
        # Safely get environment variables
        envs_dict = dict(os.environ)
    except Exception as e:
        return {"error": f"Error retrieving environment variables: {e!s}"}

    return {
        "envs": envs_dict,
        "user": user.email,
        "user_home_dir": user_home_dir,
        "user_id": uid,
        "group_id": gid,
        "user_name": user_info.pw_name,
        "group_name": group_info.gr_name,
    }


@router.get(
    "/usage",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def usage():
    return {
        "memory": get_memory_info(),
    }


def get_memory_info():
    memory_info = {}

    try:
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes") as f:  # noqa: PTH123
            memory_info["limit"] = int(f.read().strip())
    except FileNotFoundError:
        memory_info["limit"] = "N/A"

    try:
        with open("/sys/fs/cgroup/memory/memory.soft_limit_in_bytes") as f:  # noqa: PTH123
            memory_info["soft_limit"] = int(f.read().strip())
    except FileNotFoundError:
        memory_info["soft_limit"] = "N/A"

    try:
        with open("/sys/fs/cgroup/memory/memory.usage_in_bytes") as f:  # noqa: PTH123
            memory_info["usage"] = int(f.read().strip())
    except FileNotFoundError:
        memory_info["usage"] = "N/A"

    return memory_info


# @router.get(
#     "/git_clone_example",
#     dependencies=[Depends(get_current_active_superuser)],
#     status_code=201,
# )
# async def git_clone_example(
#     user: CurrentUser,  # noqa: ARG001
# ):
#     bash(
#         f"git clone https://{settings.MAIN_GH_TOKEN}@github.com/{settings.MAIN_GH_USER}/gomtm.git --depth=1 --no-single-branch {settings.STORAGE_DIR_BASE}/gomtm"
#     )


def get_disk_usage(path: str):
    try:
        usage = shutil.disk_usage(path)
        return {"total": usage.total, "used": usage.used, "free": usage.free}  # noqa: TRY300
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


# @router.get(
#     "/dist_usage",
#     dependencies=[Depends(get_current_active_superuser)],
#     status_code=201,
# )
# async def dist_usage(
#     user: CurrentUser,  # noqa: ARG001
# ):
#     disk_usage = get_disk_usage(settings.STORAGE_DIR_BASE)
#     return disk_usage


class RunBashReq(BaseModel):
    cmd: str


@router.post(
    "/bash", dependencies=[Depends(get_current_active_superuser)], status_code=201
)
async def run_bash(
    req: RunBashReq,
):
    threading.Thread(target=bash, args=(req.cmd,)).start()
    return ""


class ReadFileReq(BaseModel):
    file_path: str


@router.post(
    "/read_file", dependencies=[Depends(get_current_active_superuser)], status_code=201
)
async def read_file(
    req: ReadFileReq,
):
    try:
        if not Path.exists(req.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        with Path.open(req.file_path) as file:
            content = file.read()
        return {"content": content}

    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error reading file: {e!s}")
