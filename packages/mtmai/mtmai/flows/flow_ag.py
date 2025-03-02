from __future__ import annotations

from typing import cast

from autogen_core import SingleThreadedAgentRuntime
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp
from opentelemetry.trace import TracerProvider

from ..teams.assisant_teams import MtAssisantTeam


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
)
class FlowAg:
    def __init__(self, tracer_provider: TracerProvider | None = None) -> None:
        self._runtime = SingleThreadedAgentRuntime(
            tracer_provider=tracer_provider,
            # payload_serialization_format=self._payload_serialization_format,
        )
        logger.info("FlowAg 初始化")

    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        message = cast(AgentRunInput, input)
        cancellation_token = MtCancelToken(
            lambda_cancel=hatctx.cancel, is_cancelled=hatctx.done
        )
        # tenant_client = TenantClient()
        task = message.content
        assisant_team = MtAssisantTeam(task=task, cancellation_token=cancellation_token)
        return assisant_team.run()

        #
        # set_team_id_ctx(message.team_id)

        # return ""
