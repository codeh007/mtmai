"""
MergeAnswersNode Module
"""

from typing import List, Optional

from langchain_core.runnables import RunnableConfig

from .base_node import BaseNode


class MergeAnswersNode(BaseNode):
    """
    一个负责将多个图实例的答案合并成单一答案的节点。
    A node responsible for merging the answers from multiple graph instances into a single answer.

    Attributes:
        llm_model: An instance of a language model client, configured for generating answers.
        verbose (bool): A flag indicating whether to show print statements during execution.

    Args:
        input (str): Boolean expression defining the input keys needed from the state.
        output (List[str]): List of output keys to be updated in the state.
        node_config (dict): Additional configuration for the node.
        node_name (str): The unique identifier name for the node, defaulting to "GenerateAnswer".
    """

    def __init__(
        self,
        input: str,
        output: List[str],
        node_config: Optional[dict] = None,
        node_name: str = "MergeAnswers",
    ):
        super().__init__(node_name, "node", input, output, 2, node_config)

        self.llm_model = node_config["llm_model"]
        self.verbose = (
            False if node_config is None else node_config.get("verbose", False)
        )

    async def __call__(self, state: dict, config: RunnableConfig):
        pass
