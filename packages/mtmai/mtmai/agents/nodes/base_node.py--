"""
BaseNode Module
"""

from abc import ABC
from typing import List, Optional


class BaseNode(ABC):
    """
    基础节点类，所有节点都应该继承自这个类。
    Base node class that all nodes should inherit from.
    """

    def __init__(
        self,
        node_name: str,
        node_type: str,
        input: str,
        output: List[str],
        max_retries: int = 3,
        node_config: Optional[dict] = None,
    ):
        self.node_name = node_name
        self.node_type = node_type
