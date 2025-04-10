from autogen_agentchat.messages import TextMessage
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.social_team_config import SocialTeamConfig
from mtmai.clients.rest.models.start_new_chat_input import StartNewChatInput
from mtmai.context.context import Context
from mtmai.teams.team_social import SocialTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.SOCIAL,
    on_events=[FlowNames.SOCIAL],
)
class FlowSocial:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        # input = MtAgEvent.from_dict(hatctx.input)
        input = StartNewChatInput.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()

        if isinstance(input.config.actual_instance, SocialTeamConfig):
            team = SocialTeam._from_config(
                SocialTeamConfig.from_dict(input.config.actual_instance.model_dump())
            )
        else:
            raise ValueError(
                f"Invalid team config type: {type(input.config.actual_instance)}"
            )

        task = TextMessage(content=input.task, source="user")
        result = await team.run(task=task, cancellation_token=cancellation_token)
        logger.info(f"result: {result}")
        return result
