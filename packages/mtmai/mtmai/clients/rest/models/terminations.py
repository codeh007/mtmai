# coding: utf-8

"""
    Mtmai API

    The Mtmai API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from mtmai.clients.rest.models.function_call_termination import FunctionCallTermination
from mtmai.clients.rest.models.handoff_termination import HandoffTermination
from mtmai.clients.rest.models.max_message_termination import MaxMessageTermination
from mtmai.clients.rest.models.source_match_termination import SourceMatchTermination
from mtmai.clients.rest.models.stop_message_termination import StopMessageTermination
from mtmai.clients.rest.models.text_mention_termination import TextMentionTermination
from mtmai.clients.rest.models.timeout_termination import TimeoutTermination
from mtmai.clients.rest.models.token_usage_termination import TokenUsageTermination
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

TERMINATIONS_ONE_OF_SCHEMAS = ["FunctionCallTermination", "HandoffTermination", "MaxMessageTermination", "SourceMatchTermination", "StopMessageTermination", "TextMentionTermination", "TimeoutTermination", "TokenUsageTermination"]

class Terminations(BaseModel):
    """
    Terminations
    """
    # data type: TextMentionTermination
    oneof_schema_1_validator: Optional[TextMentionTermination] = None
    # data type: HandoffTermination
    oneof_schema_2_validator: Optional[HandoffTermination] = None
    # data type: TimeoutTermination
    oneof_schema_3_validator: Optional[TimeoutTermination] = None
    # data type: SourceMatchTermination
    oneof_schema_4_validator: Optional[SourceMatchTermination] = None
    # data type: FunctionCallTermination
    oneof_schema_5_validator: Optional[FunctionCallTermination] = None
    # data type: TokenUsageTermination
    oneof_schema_6_validator: Optional[TokenUsageTermination] = None
    # data type: MaxMessageTermination
    oneof_schema_7_validator: Optional[MaxMessageTermination] = None
    # data type: StopMessageTermination
    oneof_schema_8_validator: Optional[StopMessageTermination] = None
    actual_instance: Optional[Union[FunctionCallTermination, HandoffTermination, MaxMessageTermination, SourceMatchTermination, StopMessageTermination, TextMentionTermination, TimeoutTermination, TokenUsageTermination]] = None
    one_of_schemas: Set[str] = { "FunctionCallTermination", "HandoffTermination", "MaxMessageTermination", "SourceMatchTermination", "StopMessageTermination", "TextMentionTermination", "TimeoutTermination", "TokenUsageTermination" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = Terminations.model_construct()
        error_messages = []
        match = 0
        # validate data type: TextMentionTermination
        if not isinstance(v, TextMentionTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TextMentionTermination`")
        else:
            match += 1
        # validate data type: HandoffTermination
        if not isinstance(v, HandoffTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `HandoffTermination`")
        else:
            match += 1
        # validate data type: TimeoutTermination
        if not isinstance(v, TimeoutTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TimeoutTermination`")
        else:
            match += 1
        # validate data type: SourceMatchTermination
        if not isinstance(v, SourceMatchTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SourceMatchTermination`")
        else:
            match += 1
        # validate data type: FunctionCallTermination
        if not isinstance(v, FunctionCallTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FunctionCallTermination`")
        else:
            match += 1
        # validate data type: TokenUsageTermination
        if not isinstance(v, TokenUsageTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TokenUsageTermination`")
        else:
            match += 1
        # validate data type: MaxMessageTermination
        if not isinstance(v, MaxMessageTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `MaxMessageTermination`")
        else:
            match += 1
        # validate data type: StopMessageTermination
        if not isinstance(v, StopMessageTermination):
            error_messages.append(f"Error! Input type `{type(v)}` is not `StopMessageTermination`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in Terminations with oneOf schemas: FunctionCallTermination, HandoffTermination, MaxMessageTermination, SourceMatchTermination, StopMessageTermination, TextMentionTermination, TimeoutTermination, TokenUsageTermination. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in Terminations with oneOf schemas: FunctionCallTermination, HandoffTermination, MaxMessageTermination, SourceMatchTermination, StopMessageTermination, TextMentionTermination, TimeoutTermination, TokenUsageTermination. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # use oneOf discriminator to lookup the data type
        _data_type = json.loads(json_str).get("provider")
        if not _data_type:
            raise ValueError("Failed to lookup data type from the field `provider` in the input.")

        # check if data type is `FunctionCallTermination`
        if _data_type == "FunctionCallTermination":
            instance.actual_instance = FunctionCallTermination.from_json(json_str)
            return instance

        # check if data type is `HandoffTermination`
        if _data_type == "HandoffTermination":
            instance.actual_instance = HandoffTermination.from_json(json_str)
            return instance

        # check if data type is `MaxMessageTermination`
        if _data_type == "MaxMessageTermination":
            instance.actual_instance = MaxMessageTermination.from_json(json_str)
            return instance

        # check if data type is `SourceMatchTermination`
        if _data_type == "SourceMatchTermination":
            instance.actual_instance = SourceMatchTermination.from_json(json_str)
            return instance

        # check if data type is `StopMessageTermination`
        if _data_type == "StopMessageTermination":
            instance.actual_instance = StopMessageTermination.from_json(json_str)
            return instance

        # check if data type is `TextMentionTermination`
        if _data_type == "TextMentionTermination":
            instance.actual_instance = TextMentionTermination.from_json(json_str)
            return instance

        # check if data type is `TimeoutTermination`
        if _data_type == "TimeoutTermination":
            instance.actual_instance = TimeoutTermination.from_json(json_str)
            return instance

        # check if data type is `TokenUsageTermination`
        if _data_type == "TokenUsageTermination":
            instance.actual_instance = TokenUsageTermination.from_json(json_str)
            return instance

        # deserialize data into TextMentionTermination
        try:
            instance.actual_instance = TextMentionTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into HandoffTermination
        try:
            instance.actual_instance = HandoffTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into TimeoutTermination
        try:
            instance.actual_instance = TimeoutTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SourceMatchTermination
        try:
            instance.actual_instance = SourceMatchTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FunctionCallTermination
        try:
            instance.actual_instance = FunctionCallTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into TokenUsageTermination
        try:
            instance.actual_instance = TokenUsageTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into MaxMessageTermination
        try:
            instance.actual_instance = MaxMessageTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into StopMessageTermination
        try:
            instance.actual_instance = StopMessageTermination.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into Terminations with oneOf schemas: FunctionCallTermination, HandoffTermination, MaxMessageTermination, SourceMatchTermination, StopMessageTermination, TextMentionTermination, TimeoutTermination, TokenUsageTermination. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into Terminations with oneOf schemas: FunctionCallTermination, HandoffTermination, MaxMessageTermination, SourceMatchTermination, StopMessageTermination, TextMentionTermination, TimeoutTermination, TokenUsageTermination. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], FunctionCallTermination, HandoffTermination, MaxMessageTermination, SourceMatchTermination, StopMessageTermination, TextMentionTermination, TimeoutTermination, TokenUsageTermination]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


