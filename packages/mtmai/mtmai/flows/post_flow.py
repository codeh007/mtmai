from typing import Any

from prefect import flow

from mtmai.crud.curd_blog import create_blog_post
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.flows import FlowBase, mtflow
from mtmai.models.blog import BlogPostCreateReq
from mtmai.mtlibs import aisdk


@mtflow(BlogPostCreateReq)
class CreatePostFlow(FlowBase):
    @classmethod
    @flow(name="CreatePostFlow")
    async def execute(
        cls, session: AsyncSessionDep, current_user: CurrentUser, data: dict
    ) -> Any:
        item_in = cls.form_model(**data)
        # task1_result = await create_site_task(session, current_user, item_in)
        create_post_result = await create_blog_post(
            session=session, blog_post_create=item_in
        )
        yield aisdk.AiTextChunck("创建文章完成" + create_post_result.id)
