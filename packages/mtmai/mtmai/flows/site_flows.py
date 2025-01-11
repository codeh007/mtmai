from typing import Any

import httpx
from bs4 import BeautifulSoup
from prefect import flow, get_run_logger, task
from pydantic import BaseModel

# from mtmai.biz import biz_scheule
from mtmai.crud import crud_task
from mtmai.crud.curd_search import create_site_search_index
from mtmai.crud.curd_site import get_site_by_id, get_sites_enabled_automation
from mtmai.db.db import get_async_session
from mtmai.deps import AsyncSessionDep
from mtmai.flows import FlowBase, mtflow
from mtmai.flows.article_gen import (
    WriteSingleChapterRequest,
    article_gen_outline,
    write_book_chapter_crew,
)
from mtmai.flows.flow_publish import publish_article
from mtmai.flows.flows_util import mtflow_util
from mtmai.models.book_gen import (
    Chapter,
    GenBookState,
    WriteOutlineRequest,
)
from mtmai.models.site import (
    SiteCreateRequest,
)
from mtmai.models.task import MtTaskType


class SiteDetectInfo(BaseModel):
    title: str | None = None
    description: str | None = None


@task()
async def site_info_detect(session: AsyncSessionDep, url: str):
    """获取远程站点基本信息"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string if soup.title else None
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"] if meta_description else None
    if description:
        description = description[:100]
    return SiteDetectInfo(title=title, description=description)


@task()
async def create_site_task(
    site_id: str,
    user_id: str,
):
    logger = get_run_logger()
    try:
        logger.info(f"create_site_task 开始，site_id: {site_id}, user_id: {user_id}")
        async with get_async_session() as session:
            site = await get_site_by_id(session, site_id, user_id)
        if not site:
            logger.info(f"site_id: {site_id}, user_id: {user_id} 不存在")

        logger.info(f"工作流开始更新 site 信息 {site_id}")
        target_url = str(site.url)
        site_info = await site_info_detect(session, target_url)

        # Convert item_in to dict, convert url to string, and add owner_id
        site_data = site.model_dump()
        site_data["url"] = str(site_data["url"])  # Convert Url to string
        site_data["owner_id"] = user_id
        site.title = site_info.title
        site.description = site_info.description
        session.add(site)
        await session.commit()
        await session.refresh(site)
        await create_site_search_index(session, site, user_id)
        await session.refresh(site)
        ret = site.model_dump()
        logger.info(f"site_id: {site_id}, user_id: {user_id} 更新完成")
    except Exception as e:
        logger.error(
            f"site_id: {site_id}, user_id: {user_id} create_site_task失败: {e}"
        )
    return ret


@mtflow(SiteCreateRequest)
class CreateSiteFlow(FlowBase):
    @classmethod
    @flow(name="CreateSiteFlow")
    async def execute(cls, site_id: str, user_id: str) -> Any:
        # yield aisdk.AiTextChunck("<mtmai_response>\n")
        logger = get_run_logger()
        logger.info(f"site_id: {site_id}, user_id: {user_id}")
        async with get_async_session() as session:
            site = await get_site_by_id(session, site_id, user_id)
        if not site:
            logger.info(f"site_id: {site_id}, user_id: {user_id} 不存在")

        logger.info("工作流开始更新 site 信息")
        # try:
        #     yield aisdk.AiTextChunck("<mtmai_msg>开始处理</mtmai_msg>\n")
        #     req_model: SiteCreateRequest = cls.form_model
        #     yield aisdk.AiTextChunck("<mtmai_msg>验证数据</mtmai_msg>\n")
        #     item_in = req_model.model_validate(data)
        #     yield aisdk.AiTextChunck("<mtmai_msg>调用工作流</mtmai_msg>\n")
        #     task1_result = await create_site_task(item_in, user_id)
        #     yield aisdk.AiTextChunck("<mtmai_msg>完成</mtmai_msg>\n")
        #     yield aisdk.AiTextChunck(
        #         '<mtmai_action url="https://www.baidu.com">自动跳转</mtmai_action>\n'
        #     )
        # except ValidationError as e:
        #     yield aisdk.AiTextChunck(f"输入不正确: {e}")
        #     # pass
        # yield aisdk.AiTextChunck("</mtmai_response>\n")


@flow
async def create_site_flow(user_id: str, site_id: str):
    logger = get_run_logger()
    logger.info(f"create_site_flow user_id: {user_id}, site_id: {site_id}")

    await create_site_task(site_id, user_id)


@flow
async def flow_site_automation():
    """后台检测 site 状态，根据状态自动触发子工作流的运行"""
    async with mtflow_util() as flow_util:
        flow_util.info("开始检测 site 状态")
        async with get_async_session() as session:
            sites = await get_sites_enabled_automation(session)

        if not sites or len(sites) == 0:
            flow_util.info("没有站点启用自动化")
            return

        for site in sites:
            flow_util.info(f"开始调度 site {site.id} 的任务")
            async with get_async_session() as session:
                tasks_to_run = await crud_task.get_tasks_to_run(
                    session=session, site_id=site.id, limit=1
                )

            if not tasks_to_run or len(tasks_to_run) == 0:
                flow_util.info("没有任务需要运行, 现在创建一个文章生成任务")
                async with get_async_session() as session:
                    # TODO: 这里的参数应该 AI 生成

                    # init_state = {
                    #     "topic": "AI 在 2024 年 9 月的现状: 各行业的趋势和未来展望",
                    #     "goal": "生成一本书，介绍 AI 在 2024 年 9 月的现状，包括各行业的趋势和未来展望。",
                    # }
                    # new_mttask = await mttask_create(
                    #     session=session,
                    #     site_id=site.id,
                    #     name="gen_article",
                    #     init_state={},
                    # )
                    # await flow_run_task(str(new_mttask.id))
                    pass

            else:
                flow_util.info(f"有任务需要运行, len={len(tasks_to_run)}")
                for ta in tasks_to_run:
                    flow_util.info(f"开始执行任务: {ta}")
                    await flow_run_task(str(ta.id))

        # 新方式：根据任务计划表进行调度
        async with get_async_session() as session:
            schedules = await crud_task.list_schedult_to_run(session=session)
            flow_util.info(f"调度任务计划数量: {len(schedules)}")
            for schedule in schedules:
                await flow_run_schedule(str(schedule.id))


@flow
async def flow_run_schedule(schedule_id: str):
    """根据数据库表 schedule 的值启动对应的工作流"""
    async with mtflow_util() as flow_util:
        flow_util.info(f"开始运行 schedule {schedule_id}")
        # async with get_async_session() as session:
        #     sched = await crud_task.get_schedule(session=session, id=schedule_id)
        #     if not sched:
        #         raise ValueError(f"schedule {schedule_id} 不存在")

        #     task_to_run = None
        #     if sched.task_type == MtTaskType.ARTICLE_GEN:
        #         task_to_run = await mttask_create(
        #             session=session,
        #             schedule_id=schedule_id,
        #             name=MtTaskType.ARTICLE_GEN,
        #             init_state={
        #                 **sched.params,
        #             },
        #         )
        #     else:
        #         raise ValueError(f"未知的任务类型 {sched.task_type}")

        new_task = await biz_scheule.make_new_task_by_schedule(schedule_id)

        await flow_run_task(str(new_task.id))


@flow
async def flow_run_task(mttask_id: str):
    """根据数据库表 mttask 的值启动对应的工作流"""
    async with mtflow_util() as flow_util:
        async with get_async_session() as session:
            mttask = await crud_task.mttask_get_by_id(
                session=session, mttask_id=mttask_id
            )
        flow_util.info(f"开始运行mttask {mttask.id}")

        if not mttask:
            raise ValueError(f"mttask {mttask_id} 不存在")
        if not mttask.name:
            raise ValueError(f"mttask {mttask.id} 没有 name 值")

        # 状态判断
        if mttask.status == "new":
            flow_util.info(f"mttask {mttask.id} 状态为 new, 跳过")
            return

        task_name = mttask.name
        if mttask.status == "pending":
            match task_name:
                case MtTaskType.ARTICLE_GEN:
                    await flow_run_gen_article(mttask_id=str(mttask.id))
                case _:
                    raise ValueError(f"未知的任务类型 {mttask.name}")

            flow_util.info(f"完成 mttask {mttask.id}")


@flow
async def flow_run_gen_article(mttask_id: str):
    """
    单个站点的自动化工作流
    """
    async with mtflow_util() as flow_util:
        await flow_util.info(f"flow_site_gen mttask_id: {mttask_id}")

        async with get_async_session() as session:
            mttask = await crud_task.mttask_get_by_id(
                session=session, mttask_id=mttask_id
            )
            if not mttask:
                raise ValueError(f"mttask {mttask_id} 不存在")
            sched = await crud_task.schedule_get_by_id(
                session=session, schedule_id=mttask.schedule_id
            )
            site_id = sched.inputs.get("site_id")
            if not site_id:
                raise ValueError(f"schedule {sched.id} 没有 site_id 值")
            site = await get_site_by_id(session=session, site_id=site_id)

        flow_util.info("生成大纲 ...")
        async with get_async_session() as session:
            mttask = await crud_task.mttask_get_by_id(
                session=session, mttask_id=mttask_id
            )

        _state = mttask.state or {}
        state = GenBookState.model_validate(_state)

        if not state.title and state.topic:
            # state 为全新态
            # TODO: 这里的初始参数应该 由 AI 生成
            state.title = "AI 在 2024 年 9 月的现状: 各行业的趋势和未来展望"
            state.goal = "生成一本书，介绍 AI 在 2024 年 9 月的现状，包括各行业的趋势和未来展望。"

        outlines = await article_gen_outline(
            req=WriteOutlineRequest(
                topic=state.topic,
                goal=state.goal,
            )
        )
        await flow_util.info(f"flow_article_gen end, outlines: {outlines}")

        if not outlines:
            flow_util.info("大纲编写失败")
            return
        await flow_util.info("大纲编写完成，开始写内容")

        async with get_async_session() as session:
            await crud_task.mttask_update_state(
                session=session, mttask_id=mttask_id, state=state
            )

        chapters = outlines.chapters
        state.book_outline = chapters

        chapters = []
        for index, chapter_outline in enumerate(state.book_outline, start=1):
            flow_util.info(
                f"开始写章节正文 {index}/{len(state.book_outline)}: {chapter_outline.title}"
            )
            output = await write_book_chapter_crew(
                req=WriteSingleChapterRequest(
                    goal=state.goal,
                    topic=state.topic,
                    chapter_title=chapter_outline.title,
                    chapter_description=chapter_outline.description,
                    book_outlines=state.book_outline,
                )
            )
            if not output:
                await flow_util.info(f"写章节正文失败: {output}")
                continue
            chapters.append(Chapter(title=output.title, content=output.content))

        state.book.extend(chapters)
        # sections = [await write_section(topic) for topic in outline]
        await flow_util.info(f"章节内容写入完成, 章节数量:{len(chapters)}")
        await publish_article(site_id=site.id, state=state)
    # except litellm.RateLimitError as e:
    #     flow_util.error(f"调用大模型到达限制，TODO 切换大模型: {e}")
    #     raise e
    # except Exception as e:
    #     flow_util.error(f"flow_site_gen 失败: {e}")
    #     raise e
