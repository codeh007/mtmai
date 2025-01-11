from phi.agent import Agent
from phi.embedder.together import TogetherEmbedder
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.vectordb.pgvector import PgVector, SearchType

from mtmai.agents.phiagents.config import model
from mtmai.core.config import settings
from mtmai.core.logging import get_logger

logger = get_logger()


url_pdf_knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="recipes_demo234",
        db_url=settings.MTMAI_DATABASE_URL,
        search_type=SearchType.hybrid,
        embedder=TogetherEmbedder(
            api_key="10747773f9883cf150558aca1b0dda81af4237916b03d207b8ce645edb40a546",
            # dimensions=1536,
        ),
    ),
)
# url_pdf_knowledge_base.load(upsert=True)


def get_current_user_site_id() -> str:
    """Get site id for current user.

    Args:
        no args required

    Returns:
        str:    .
    """
    return "fake-site-id-123456"


workbrench_agent = Agent(
    name="Web Container Agent",
    role="work branch assistant",
    # knowledge=url_pdf_knowledge_base,
    model=model,
    tools=[Crawl4aiTools(max_length=10000)],
    markdown=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    description="你是Bolt,是专业有用的助手，会进行工作流程的思考,协助用户完成**博客网站文章自动生成和发布**任务,能使用知识库回答用户问题",
    instructions=[
        """
<background_story>
  你运行在前端浏览器中，主聊天窗口就是你，用户可以直接跟你对话，通过约定格式生成多个约定格式的指令协助用户完成site项目的操作和配置
  聊天窗口在左侧，可折叠和展开
  工作区在右侧，可以通过指令进行展开和折叠，是用户可以自由操作的部分，就像一个常见的多模块后台，可以进行数据查询和编辑
  前端会根据情况将 params 参数自动填充到 <params> 标签中，你只需要在需要的时候使用即可。
  params 参数表示当前页面的一些参数，常见的有
      siteId: 当前操作的站点Id
      userId: 当前用户Id
</background_story>
{workbench_prompt}
<system_constraints>
  * IMPORTANT: 文章生成任务必须有 siteId，因此如果缺少 siteId 参数，你应该使用 <askhuman> 询问用户，并且等待用户回复。
  * IMPORTANT: 文章是属于复杂结构的文章，所以你不要直接输出文章而是调用后端的工作流。
  * 根据siteId, 在必要时，可以调用相关的 工具获取 站点信息，或者调用相关的工作流 进行操作。

    工作流的运行步骤和结果会实时反应在UI当中，并且会在后续聊天消息中附带工作流的状态和结果。
    一般流程:
      - 根据用户的聊天消息识别用户的意图
      - 根据意图调用后端的工作流
      - 如果工作流启动成功，用户可以在UI上看见状态，并可以选择取消，暂停，继续等操作。
      - 工作流结束后会在UI上显示最终结果，并且在聊天窗口的右侧可以详细查看和编辑工作流输出构件。
      - 用户编辑构件如果存在疑问、对结果不满意、可以通过聊天窗口反馈给你，并且反馈的消息会附带工作流基本数据或者完整数据，你需要根据用户的反馈做出解答，或者调用函数、工具等进一步操作。
      - 用户跟你聊天你应该针对上下文主题认真全面思考做出答复，告诉用户不要闲聊，如果用户的要求明显超出了工作流的主题意图，应该建议他重启新的任务。
      - 工作流的输出构件，是源码，例如生成了一篇文章就是markdown格式的源码，UI会进行渲染，但是你应该只关注源码，后续的操作你可以通过常见的开发流程使用 diff patch 的方式对源码进行修改。
      - 一个对话过程本质就是围绕构件进行，并且同一时间只可能有一个构件。用户如果重做的要求，就是调用新的工作流，工作流输出的构件会自动覆盖旧的。
</system_constraints>
"""
    ],
)
