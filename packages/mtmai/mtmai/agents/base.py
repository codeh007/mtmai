import abc


class GraphBuilder(abc.ABC):
    from langgraph.graph import StateGraph

    @abc.abstractmethod
    async def build_graph(self) -> StateGraph:
        pass

    @property
    def name(self) -> str:
        """作为功能节点的节点名称"""
        return self.__class__.__name__

    @property
    def description(self) -> str:
        """作为功能节点的描述"""
        return self.__class__.__doc__ or ""
