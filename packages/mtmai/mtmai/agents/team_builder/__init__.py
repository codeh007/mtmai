from .article_gen_teambuilder import ArticleGenTeamBuilder
from .assisant_team_builder import AssistantTeamBuilder
from .demo_human_in_loop import DemoHumanInLoopTeamBuilder
from .m1_web_builder import M1WebTeamBuilder
from .swram_team_builder import SwramTeamBuilder
from .travel_builder import TravelTeamBuilder

current_team_version = 1


# default_team_name = "assistant_team"
default_team_name = "demo_human_in_loop"

team_builders = [
    AssistantTeamBuilder(),
    SwramTeamBuilder(),
    ArticleGenTeamBuilder(),
    M1WebTeamBuilder(),
    TravelTeamBuilder(),
    DemoHumanInLoopTeamBuilder(),
]


team_builder_map = {team_builder.name: team_builder for team_builder in team_builders}
