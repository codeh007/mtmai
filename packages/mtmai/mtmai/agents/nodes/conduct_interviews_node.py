from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import END, StateGraph

from mtmai.agents.nodes import gen_answer_node
from mtmai.agents.nodes.generate_question import GenQuestionNode
# from mtmai.agents.states.research_state import InterviewState, ResearchState
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import InterviewState, ResearchState

logger = get_logger()

InterviewState
def route_messages(state: InterviewState, name: str = "Subject_Matter_Expert"):
    max_num_turns = 3
    messages = state["messages"]
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )
    if num_responses >= max_num_turns:
        return END
    last_question = messages[-2]
    if last_question.content.endswith("Thank you so much for your help!"):
        return END
    return "continue"


# 旧版 (基于 langgraph)
class ConductInterviewNode:
    def __init__(
        self,
        runnable: Runnable,
    ):
        self.runnable = runnable

    def node_name(self):
        return "conduct_interview_node"

    async def __call__(self, state: ResearchState, config: RunnableConfig):
        topic = state["topic"]

        # 前面步骤确定了 问题解答专家的角色(editor), 现在动态构建自动，并发对多个专家进行采访，看他们观点
        initial_states = [
            {
                "editor": editor,
                "messages": [
                    AIMessage(
                        content=f"So you said you were writing an article on {topic}?",
                        name="Subject_Matter_Expert",
                    )
                ],
            }
            for editor in state["editors"]
        ]
        # We call in to the sub-graph here to parallelize the interviews

        builder = StateGraph(InterviewState)

        builder.add_node("ask_question", GenQuestionNode(self.runnable))
        builder.add_node(
            "answer_question",
            gen_answer_node.GenAnswerNode(
                self.runnable, name="Subject_Matter_Expert", max_str_len=15000
            ),
        )
        builder.add_conditional_edges(
            "answer_question",
            route_messages,
            {
                "continue": "ask_question",
                "error": END,
                END: END,
            },
        )
        builder.add_edge("ask_question", "answer_question")

        builder.set_entry_point("ask_question")
        interview_graph = builder.compile().with_config(run_name="Conduct Interviews")

        logger.info(f"开始进行 采访, 数量: {len(initial_states)}")

        enabled_batch = False
        if enabled_batch:
            interview_results = await interview_graph.abatch(initial_states, config)
        else:
            interview_results = []
            first_state = initial_states[0]
            # for a in initial_states:
            #     interview_results.append(await interview_graph.ainvoke(a))
            # 暂时仅处理第一个
            interview_results.append(await interview_graph.ainvoke(first_state))
        # logger.info(f"采访结束, 数量: {len(interview_results)}")
        return {
            **state,
            "interview_results": interview_results,
        }


class ConductInterviewNodeV2:
    def __init__(
        self,
        runnable: Runnable,
    ):
        self.runnable = runnable

    def node_name(self):
        return "conduct_interview_node"

    async def __call__(self, state: ResearchState):
        topic = state["topic"]

        # 前面步骤确定了 问题解答专家的角色(editor), 现在动态构建自动，并发对多个专家进行采访，看他们观点
        initial_states = [
            {
                "editor": editor,
                "messages": [
                    AIMessage(
                        content=f"So you said you were writing an article on {topic}?",
                        name="Subject_Matter_Expert",
                    )
                ],
            }
            for editor in state["editors"]
        ]
        # We call in to the sub-graph here to parallelize the interviews

        builder = StateGraph(InterviewState)

        builder.add_node("ask_question", GenQuestionNode(self.runnable))
        builder.add_node(
            "answer_question",
            gen_answer_node.GenAnswerNode(
                self.runnable, name="Subject_Matter_Expert", max_str_len=15000
            ),
        )
        builder.add_conditional_edges(
            "answer_question",
            route_messages,
            {
                "continue": "ask_question",
                "error": END,
                END: END,
            },
        )
        builder.add_edge("ask_question", "answer_question")

        builder.set_entry_point("ask_question")
        interview_graph = builder.compile().with_config(run_name="Conduct Interviews")

        logger.info(f"开始进行 采访, 数量: {len(initial_states)}")

        enabled_batch = False
        if enabled_batch:
            interview_results = await interview_graph.abatch(initial_states, config)
        else:
            interview_results = []
            first_state = initial_states[0]
            # for a in initial_states:
            #     interview_results.append(await interview_graph.ainvoke(a))
            # 暂时仅处理第一个
            interview_results.append(await interview_graph.ainvoke(first_state))
        # logger.info(f"采访结束, 数量: {len(interview_results)}")
        return {
            **state,
            "interview_results": interview_results,
        }
