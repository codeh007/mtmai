import base64
import logging

import httpx
from fastapi import APIRouter, Path
from fastapi.responses import PlainTextResponse
from github import Auth

from mtmai.core.config import settings
from mtmlib import github

router = APIRouter()


@router.get("/down/{dataset_path:path}")
def dataset_download(dataset_path: str = Path(...)):
    """数据集文件下载,(内部从 github 仓库获取数据集文件)"""
    auth = Auth.Token(settings.MAIN_GH_TOKEN)
    g = github(auth=auth)
    repo = g.get_repo("codeh007/mtdataset")
    contents = repo.get_contents(dataset_path)
    if contents.content:
        # 直接返回了内容响应
        decoded_content = base64.b64decode(contents.content)
        g.close()
        return PlainTextResponse(content=decoded_content)
    elif contents.download_url:
        # 返回下载地址, 一般是因为内容较大
        # TODO: 流式传输和, 否则可能撑爆内存.
        resp = httpx.get(contents.download_url)
        content = resp.text
        g.close()
        return content
    msg = "github 未知的响应内容"
    raise Exception(msg)  # noqa: TRY002


router = APIRouter()

queue_tran = "trans"
logger = logging.getLogger()


# @router.get("/tran_guwen")
# async def run_tran_guwen(
#     queue: MqDep,
# ):
#     """古文训练"""
#     queue.create_queue(queue_tran)
#     logger.info("开始训练模型 guwen")
#     queue.send(queue_tran, {"params1": "param1"})
#     return {"ok": True}


# @router.get("/tran_clickbait")
# async def tran_clickbait():
#     """模型训练例子1"""
#     threading.Thread(target=start_trans_clickbait).start()
#     return ""


# def start_worker_main():
#     if coreutils.is_in_testing():
#         return
#     if not coreutils.is_in_gitpod():
#         return

#     workermain = WorkerMain(queue=get_queue())
#     workermain.register_consumer(queue_name=queue_tran, consumer_fn=tran_guwen_consumer)
#     workermain.run()
