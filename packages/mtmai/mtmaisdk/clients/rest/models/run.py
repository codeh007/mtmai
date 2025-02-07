# coding: utf-8

"""
    Mtmai API

    The Mtmai API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from mtmaisdk.clients.rest.models.agent_message_config import AgentMessageConfig
from mtmaisdk.clients.rest.models.api_resource_meta import APIResourceMeta
from mtmaisdk.clients.rest.models.chat_message import ChatMessage
from typing import Optional, Set
from typing_extensions import Self

class Run(BaseModel):
    """
    Run
    """ # noqa: E501
    metadata: APIResourceMeta
    status: StrictStr
    task: AgentMessageConfig
    team_result: Dict[str, Any]
    messages: List[ChatMessage]
    error_message: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["metadata", "status", "task", "team_result", "messages", "error_message"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Run from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        # override the default output from pydantic by calling `to_dict()` of task
        if self.task:
            _dict['task'] = self.task.to_dict()
        # override the default output from pydantic by calling `to_dict()` of team_result
        if self.team_result:
            _dict['team_result'] = self.team_result.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in messages (list)
        _items = []
        if self.messages:
            for _item_messages in self.messages:
                if _item_messages:
                    _items.append(_item_messages.to_dict())
            _dict['messages'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Run from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "metadata": APIResourceMeta.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "status": obj.get("status"),
            "task": AgentMessageConfig.from_dict(obj["task"]) if obj.get("task") is not None else None,
            "team_result": TeamResult.from_dict(obj["team_result"]) if obj.get("team_result") is not None else None,
            "messages": [ChatMessage.from_dict(_item) for _item in obj["messages"]] if obj.get("messages") is not None else None,
            "error_message": obj.get("error_message")
        })
        return _obj


