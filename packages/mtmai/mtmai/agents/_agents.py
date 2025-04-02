sales_agent_topic_type = "SalesAgent"
issues_and_repairs_agent_topic_type = "IssuesAndRepairsAgent"
triage_agent_topic_type = "TriageAgent"
# human_agent_topic_type = "HumanAgent"
# user_topic_type = "User"
# run_team_topic_type = "RunTeam"
reviewer_agent_topic_type = "ReviewerAgent"
# coder_agent_topic_type = "CoderAgent"
team_runner_topic_type = "TeamRunner"
# browser_topic_type = "Browser"
# router_topic_type = "Router"
platform_account_topic_type = "PlatformAccount"
scheduling_assistant_topic_type = "scheduling_assistant_conversation"
# instagram_agent_topic_type = "InstagramAgent"


# class MtWebUserProxyAgent(UserProxyAgent):
#     """扩展 UserProxyAgent"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def _to_config(self) -> UserProxyAgentConfig:
#         # TODO: Add ability to serialie input_func
#         return UserProxyAgentConfig(
#             name=self.name, description=self.description, input_func=None
#         )


# class MtRoundRobinGroupChatConfig(RoundRobinGroupChatConfig):
#     """扩展 RoundRobinGroupChatConfig"""

#     # user_proxy_agent_name: str = "user_proxy_agent"
#     pass


# class MtRoundRobinGroupChat(
#     RoundRobinGroupChat, Component[MtRoundRobinGroupChatConfig]
# ):
#     """扩展 RoundRobinGroupChat"""

#     component_provider_override = "mtmai.agents._agents.RoundRobinGroupChat"

#     def __init__(
#         self,
#         participants: List[ChatAgent],
#         termination_condition: TerminationCondition | None = None,
#         max_turns: int | None = None,
#     ):
#         super().__init__(participants, termination_condition, max_turns)
