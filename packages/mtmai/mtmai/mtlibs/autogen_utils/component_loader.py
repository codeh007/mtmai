from __future__ import annotations

import importlib
from typing import Any, Dict, Type, cast, overload

from autogen_core import ComponentModel, is_component_class
from autogen_core._component_config import WELL_KNOWN_PROVIDERS
from pydantic import BaseModel
from typing_extensions import Self, TypeVar

ExpectedType = TypeVar("ExpectedType")

WELL_KNOWN_PROVIDERS = WELL_KNOWN_PROVIDERS | {
    "SocialTeam": "mtmai.teams.team_social.SocialTeam",
    "AssistantAgent": "mtmai.agents.assistant_agent.AssistantAgent",
    "InstagramAgent": "mtmai.agents.instagram_agent.InstagramAgent",
    "CodeExecutorAgent": "autogen_agentchat.agents.CodeExecutorAgent",
    "SocietyOfMindAgent": "autogen_agentchat.agents.SocietyOfMindAgent",
    "UserProxyAgent": "mtmai.agents.userproxy_agent.UserProxyAgent",
    "RoundRobinGroupChat": "autogen_agentchat.teams.RoundRobinGroupChat",
    "SelectorGroupChat": "autogen_agentchat.teams.SelectorGroupChat",
    "OpenAIChatCompletionClient": "mtmai.model_client.MtOpenAIChatCompletionClient",
    "TextMentionTermination": "autogen_agentchat.conditions.TextMentionTermination",
    "HandoffTermination": "autogen_agentchat.conditions.HandoffTermination",
    "TimeoutTermination": "autogen_agentchat.conditions.TimeoutTermination",
    "SourceMatchTermination": "autogen_agentchat.conditions.SourceMatchTermination",
    "FunctionCallTermination": "autogen_agentchat.conditions.FunctionCallTermination",
    "TokenUsageTermination": "autogen_agentchat.conditions.TokenUsageTermination",
    "MaxMessageTermination": "autogen_agentchat.conditions.MaxMessageTermination",
    "StopMessageTermination": "autogen_agentchat.conditions.StopMessageTermination",
}


class ComponentLoader:
    """
    原因: augogen 自带的 ComponentLoader 在加载 openapi 生成的 model 时有bug.
    特别是: oneOf 的字段, 使用 model_validate 不能正确解释, 应该使用 from_dict 方法.

    """

    @overload
    @classmethod
    def load_component(
        cls, model: ComponentModel | Dict[str, Any], expected: None = None
    ) -> Self: ...

    @overload
    @classmethod
    def load_component(
        cls, model: ComponentModel | Dict[str, Any], expected: Type[ExpectedType]
    ) -> ExpectedType: ...

    @classmethod
    def load_component(
        cls,
        model: ComponentModel | BaseModel | Dict[str, Any],
        expected: Type[ExpectedType] | None = None,
    ) -> Self | ExpectedType:
        # Use global and add further type checks

        if hasattr(model, "to_dict"):
            # 如果 model 是 openapi 生成的,先转换为dict
            model = model.to_dict()
        if isinstance(model, dict):
            loaded_model = ComponentModel(**model)
        else:
            loaded_model = model

        # First, do a look up in well known providers
        if loaded_model.provider in WELL_KNOWN_PROVIDERS:
            loaded_model.provider = WELL_KNOWN_PROVIDERS[loaded_model.provider]

        output = loaded_model.provider.rsplit(".", maxsplit=1)
        if len(output) != 2:
            raise ValueError("Invalid")

        module_path, class_name = output
        module = importlib.import_module(module_path)
        component_class = module.__getattribute__(class_name)

        if not is_component_class(component_class):
            raise TypeError("Invalid component class")

        # We need to check the schema is valid
        if not hasattr(component_class, "component_config_schema"):
            raise AttributeError("component_config_schema not defined")

        if not hasattr(component_class, "component_type"):
            raise AttributeError("component_type not defined")

        loaded_config_version = (
            loaded_model.component_version or component_class.component_version
        )
        if loaded_config_version < component_class.component_version:
            try:
                instance = component_class._from_config_past_version(
                    loaded_model.config, loaded_config_version
                )  # type: ignore
            except NotImplementedError as e:
                raise NotImplementedError(
                    f"Tried to load component {component_class} which is on version {component_class.component_version} with a config on version {loaded_config_version} but _from_config_past_version is not implemented"
                ) from e
        else:
            schema = component_class.component_config_schema  # type: ignore
            if hasattr(schema, "from_dict"):
                # 使用 from_dict 方法. 加载 由 openapi 生成的类 .
                validated_config = schema.from_dict(loaded_model.config)
            else:
                # autogen 默认
                validated_config = schema.model_validate(loaded_model.config)
            instance = component_class._from_config(validated_config)  # type: ignore

        if expected is None and not isinstance(instance, cls):
            raise TypeError("Expected type does not match")
        elif expected is None:
            return cast(Self, instance)
        elif not isinstance(instance, expected):
            raise TypeError("Expected type does not match")
        else:
            return cast(ExpectedType, instance)
