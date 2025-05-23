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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from mtmai.clients.rest.models.memory_config import MemoryConfig
from mtmai.clients.rest.models.model_component import ModelComponent
from mtmai.clients.rest.models.tool_component import ToolComponent
from typing import Optional, Set
from typing_extensions import Self

class SmolAgentConfig(BaseModel):
    """
    SmolAgentConfig
    """ # noqa: E501
    name: StrictStr
    description: StrictStr
    model_context: Optional[Dict[str, Any]] = None
    memory: Optional[MemoryConfig] = None
    model_client_stream: StrictBool
    system_message: Optional[StrictStr] = None
    model_client: ModelComponent
    tools: List[ToolComponent]
    handoffs: List[StrictStr]
    reflect_on_tool_use: StrictBool
    tool_call_summary_format: StrictStr
    api_key: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["name", "description", "model_context", "memory", "model_client_stream", "system_message", "model_client", "tools", "handoffs", "reflect_on_tool_use", "tool_call_summary_format", "api_key"]

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
        """Create an instance of SmolAgentConfig from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of memory
        if self.memory:
            _dict['memory'] = self.memory.to_dict()
        # override the default output from pydantic by calling `to_dict()` of model_client
        if self.model_client:
            _dict['model_client'] = self.model_client.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in tools (list)
        _items = []
        if self.tools:
            for _item_tools in self.tools:
                if _item_tools:
                    _items.append(_item_tools.to_dict())
            _dict['tools'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SmolAgentConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "model_context": obj.get("model_context"),
            "memory": MemoryConfig.from_dict(obj["memory"]) if obj.get("memory") is not None else None,
            "model_client_stream": obj.get("model_client_stream") if obj.get("model_client_stream") is not None else False,
            "system_message": obj.get("system_message"),
            "model_client": ModelComponent.from_dict(obj["model_client"]) if obj.get("model_client") is not None else None,
            "tools": [ToolComponent.from_dict(_item) for _item in obj["tools"]] if obj.get("tools") is not None else None,
            "handoffs": obj.get("handoffs"),
            "reflect_on_tool_use": obj.get("reflect_on_tool_use") if obj.get("reflect_on_tool_use") is not None else False,
            "tool_call_summary_format": obj.get("tool_call_summary_format") if obj.get("tool_call_summary_format") is not None else '{result}',
            "api_key": obj.get("api_key")
        })
        return _obj


