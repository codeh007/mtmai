from typing import Literal, Sequence

from fastapi import APIRouter
from pydantic import BaseModel

from mtmai.core.logging import get_logger
from mtmai.crud.curd_search import search_list
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.models.listview import ListVieweRsponse, ListviewItemPublic, ListviewRequest
from mtmai.models.search_index import SearchIndex, SearchRequest

router = APIRouter()
logger = get_logger()


class ListViewConfigRequest(BaseModel):
    displayAt: Literal["side", "workbench"] | None = None
    appType: Literal["mtmai", "mtmai_copilot"] | None = None
    dataType: Literal["site", "doc", "task", "kb"] | None = None


@router.post("/listview_config", response_model=ListviewRequest)
async def listview_config(
    session: AsyncSessionDep, current_user: CurrentUser, req: ListViewConfigRequest
):
    """
    获取列表视图配置

    """
    result = ListviewRequest()
    return result


@router.post("/", response_model=ListVieweRsponse)
async def listview_search(
    session: AsyncSessionDep, current_user: CurrentUser, req: ListviewRequest
):
    """
    综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。
    """
    count, items = await search_list(
        session,
        SearchRequest(
            q=req.q,
            dataType=req.dataType,
            limit=req.limit,
            skip=req.skip,
            app=req.app,
        ),
        user_id=current_user.id,
    )

    # 根据数据库搜索结构构建列表视图
    dataType = req.dataType
    if dataType == "site":
        pass
    elif dataType == "doc":
        pass
    elif dataType == "kb":
        pass
    else:
        pass
    return ListVieweRsponse(count=count, items=conver_search_result_to_list_item(items))


def conver_search_result_to_list_item(search_result: Sequence[SearchIndex]):
    list_items = []
    for item in search_result:
        list_item = ListviewItemPublic(
            id=str(item.id),
            title=item.title,
            dataType=item.content_type,
            description=item.description,
            content_id=str(item.content_id),
            # url=item.url,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        list_items.append(list_item)
    return list_items
