from fastapi import APIRouter
from pydantic import BaseModel
import structlog
from mtmai.deps import OptionalUserDep, SessionDep
from mtmai.models.chat import (
    AssisantConfig,
    AssisantMenus,
    AssisantStart,
    AssisantWelcome,
    AssisantWorkbenchConfig,
    AssisantWorkBrench,
    ListViewProps,
    SiderViewConfig,
)

router = APIRouter()
LOG = structlog.get_logger()



class WorkbenchConfigRequest(BaseModel):
    profile: str


@router.post("/workbench/config", response_model=AssisantConfig)
async def workbench_config(
    request: WorkbenchConfigRequest, user: OptionalUserDep, db: SessionDep
):
    # assistant_agent = await get_assistant_agent(request.profile)
    # config = await assistant_agent.get_config()
    # return config
    assisantConfig = AssisantConfig(
        chatProfile="site",
        logo="https://www.baidu.com/favicon.ico",
        welcome=AssisantWelcome(
            title="创意的起点",
            description="将想法变为现实",
        ),
        workbench=AssisantWorkbenchConfig(
            workbench_default="",
            workbenchs=[
                AssisantWorkBrench(id="site", label="站点", description="站点设置"),
                AssisantWorkBrench(id="article", label="文章", description="文章管理"),
                AssisantWorkBrench(id="task", label="任务", description="任务管理"),
            ],
        ),
        starts=[
            AssisantStart(
                title="自动帮我生成3篇文章并自动发布，尽量不需要我来确认你自主操作即可"
            ),
            AssisantStart(title="写一篇关于AI的文章"),
            AssisantStart(title="使用 Tailwind 构建一个 React 待办事项应用"),
            AssisantStart(title="使用 Material UI 创建一个 cookie 同意表单"),
            AssisantStart(title="使用 Astro 构建一个简单的博客"),
            AssisantStart(title="制作一个太空侵略者游戏"),
            AssisantStart(title="如何让一个 div 居中？"),
        ],
        siderView=SiderViewConfig(
            id="site_sider",
            label="Site",
            viewName="site",
            viewProps=ListViewProps(
                enableSearch=True,
                enableCreate=True,
                dataType="site",
            ).model_dump(),
        ),
        menus=[
            AssisantMenus(
                id="site",
                label="站点",
                viewName="listview",
                icon="site",
                children=[
                    AssisantMenus(
                        id="edit_site",
                        label="站点设置",
                        viewName="site_update",
                        icon="setting",
                        target="workbench",
                        viewProps=ListViewProps(
                            # dataType="site",
                            # enableSearch=True,
                            # enableCreate=True,
                            # additionActions=[
                            #     ListViewItemAdditionActions(
                            #         label="切换为当前",
                            #         icon="switch",
                            #         action="site.set_activate",
                            #     )
                            # ],
                        ).model_dump(),
                    ),
                    AssisantMenus(
                        id="site_create",
                        label="新建站点",
                        viewName="site_create",
                        icon="plus",
                    ),
                ],
            ),
            AssisantMenus(
                id="task",
                label="任务",
                viewName="listview",
                icon="task",
                children=[
                    AssisantMenus(
                        id="listview_task",
                        label="任务查询",
                        viewName="listview",
                        icon="search",
                        target="workbench",
                        viewProps=ListViewProps(
                            dataType="mttask",
                            enableSearch=True,
                            enableCreate=True,
                        ).model_dump(),
                    ),
                    AssisantMenus(
                        id="create_mttask",
                        label="新建任务",
                        viewName="create_mttask",
                        icon="plus",
                    ),
                ],
            ),
            AssisantMenus(
                id="article",
                label="文章",
                viewName="listview",
                icon="article",
                children=[
                    AssisantMenus(
                        id="listview_post",
                        label="文章查询",
                        viewName="listview",
                        icon="search",
                        target="workbench",
                        viewProps=ListViewProps(
                            dataType="post",
                            enableSearch=True,
                            enableCreate=False,
                        ).model_dump(),
                    ),
                    AssisantMenus(
                        id="create_post",
                        label="新建文章",
                        viewName="create_post",
                        icon="plus",
                    ),
                ],
            ),
        ],
    )

    if user and user.is_superuser:
        assisantConfig.menus.extend(
            [
                AssisantMenus(
                    id="user",
                    label="管理",
                    viewName="admin",
                    icon="admin",
                    children=[
                        AssisantMenus(
                            id="user", label="用户", viewName="user", icon="user"
                        ),
                        AssisantMenus(
                            id="dev",
                            label="开发工具",
                            viewName="devtools",
                            icon="devtools",
                            children=[
                                AssisantMenus(
                                    id="devtools",
                                    label="devtools",
                                    viewName="devtools",
                                )
                            ],
                        ),
                    ],
                ),
            ]
        )
    return assisantConfig
