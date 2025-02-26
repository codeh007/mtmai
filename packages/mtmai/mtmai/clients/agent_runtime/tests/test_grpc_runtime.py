import os

import pytest
from autogen_core import AgentId, AgentInstantiationContext, AgentType
from dotenv import load_dotenv
from mtmai.clients.agent_runtime.mtm_runtime import GrpcWorkerAgentRuntime
from mtmai.tests.autogen_test_utils import CascadingAgent, NoopAgent
from mtmai.tests.autogen_test_utils.telemetry_test_utils import (
    MyTestExporter,
    get_test_tracer_provider,
)
from opentelemetry.sdk.trace import TracerProvider

test_exporter = MyTestExporter()

envFileAbsPath = os.path.abspath("../gomtm/env/mtmai.env")
load_dotenv(envFileAbsPath)


@pytest.fixture
def tracer_provider() -> TracerProvider:
    test_exporter.clear()
    return get_test_tracer_provider(test_exporter)


@pytest.mark.asyncio
async def test_grpc_runtime():
    print("test_abc")


@pytest.mark.asyncio
async def test_agent_type_register_factory() -> None:
    # runtime = SingleThreadedAgentRuntime()
    runtime = GrpcWorkerAgentRuntime(tracer_provider=test_exporter)

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
