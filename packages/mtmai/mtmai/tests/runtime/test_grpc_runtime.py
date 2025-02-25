import os

import pytest
from autogen_core import AgentId, AgentInstantiationContext, AgentType
from dotenv import load_dotenv
from mtmai.tests.autogen_test_utils import CascadingAgent, NoopAgent
from mtmai.tests.autogen_test_utils.telemetry_test_utils import MyTestExporter
from worker._worker_runtime import MtmWorkerRuntime

test_exporter = MyTestExporter()

envFileAbsPath = os.path.abspath("../gomtm/env/mtmai.env")
load_dotenv(envFileAbsPath)


@pytest.mark.asyncio
async def test_grpc_runtime():
    print("test_abc")


@pytest.mark.asyncio
async def test_agent_type_register_factory() -> None:
    # runtime = SingleThreadedAgentRuntime()
    runtime = MtmWorkerRuntime(tracer_provider=test_exporter)

    def agent_factory() -> NoopAgent:
        id = AgentInstantiationContext.current_agent_id()
        assert id == AgentId("name1", "default")
        agent = NoopAgent()
        assert agent.id == id
        return agent

    await runtime.register_factory(
        type=AgentType("name1"), agent_factory=agent_factory, expected_class=NoopAgent
    )

    with pytest.raises(ValueError):
        # This should fail because the expected class does not match the actual class.
        await runtime.register_factory(
            type=AgentType("name1"),
            agent_factory=agent_factory,  # type: ignore
            expected_class=CascadingAgent,
        )

    # Without expected_class, no error.
    await runtime.register_factory(type=AgentType("name2"), agent_factory=agent_factory)
