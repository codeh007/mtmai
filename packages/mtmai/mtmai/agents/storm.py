import logging

from langgraph.graph import END, StateGraph

from mtmai.agents.conditions import condition_error_edge
from mtmai.agents.graphs.abstract_graph import AbstractGraph
from mtmai.agents.nodes.conduct_interviews_node import ConductInterviewNode
from mtmai.agents.nodes.index_references_node import IndexReferencesNode
from mtmai.agents.nodes.initialize_research_node import InitializeResearchNode
from mtmai.agents.nodes.refine_outline_node import RefineOutlineNode
from mtmai.agents.nodes.write_article_node import WriteArticleNode
from mtmai.agents.nodes.write_sections_node import WriteSectionsNode
from mtmai.llm.llm import get_llm_chatbot_default
from mtmai.models.graph_config import ResearchState

logger = logging.getLogger()


class StormGraph(AbstractGraph):
    def create_graph(self) -> StateGraph:
        # wf = StateGraph(MainState)
        # wf.add_node("human_input", HumanInputNode())
        # child_graph = self.create_sub_graph_storm().compile()

        # async def call_storm_graph(
        #     state: MainState, config: RunnableConfig
        # ) -> MainState:
        #     try:
        #         child_graph_input = {"topic": state.get("prompt")}
        #         child_graph_output = await child_graph.ainvoke(
        #             child_graph_input, config
        #         )

        #         # 输出的结果是文章生成结果
        #         logger.info(f"文章生成 结果: {child_graph_output}")

        #         return {
        #             "messages": [
        #                 ChatMessage(role="assistant", content=state.get("生成结束"))
        #             ]
        #         }
        #     except Exception as e:
        #         logger.error(f"生成文章失败: {e}")
        #         import traceback

        #         error_message = (
        #             f"生成文章失败: {e}\n\nDebug Stack:\n{traceback.format_exc()}"
        #         )
        #         logger.error(error_message)
        #         return {
        #             "messages": [ChatMessage(role="assistant", content="生成文章失败")]
        #         }

        # wf.add_node("storm", call_storm_graph)
        # wf.set_entry_point("human_input")
        # wf.add_edge("human_input", "storm")
        # wf.add_edge("storm", END)

        # return wf
        return self.create_sub_graph_storm()

    def create_sub_graph_storm(self):
        """创建 storm 子图"""
        wf = StateGraph(ResearchState)
        llm = get_llm_chatbot_default()
        wf.add_node("init_research", InitializeResearchNode(runnable=llm))
        wf.add_node("conduct_interviews", ConductInterviewNode(runnable=llm))
        wf.add_node("refine_outline", RefineOutlineNode(runnable=llm))
        wf.add_node("index_references", IndexReferencesNode(runnable=llm))
        wf.add_node("write_sections", WriteSectionsNode(runnable=llm))
        wf.add_node("write_article", WriteArticleNode(runnable=llm))
        # 添加边
        wf.add_conditional_edges(
            "init_research",
            condition_error_edge,
            {
                "continue": "conduct_interviews",
                "error": END,
            },
        )
        wf.add_conditional_edges(
            "conduct_interviews",
            condition_error_edge,
            {
                "continue": "refine_outline",
                "error": END,
            },
        )
        wf.add_conditional_edges(
            "refine_outline",
            condition_error_edge,
            {
                "continue": "index_references",
                "error": END,
            },
        )
        wf.add_edge("index_references", "write_sections")
        wf.add_edge("write_sections", "write_article")
        wf.add_edge("write_article", END)

        wf.set_entry_point("init_research")

        return wf
