# coding: utf-8

"""
    Gomtm API

    The Gomtm API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class SbOutboundCreate(BaseModel):
    """
    Create a new sing-box outbound
    """ # noqa: E501
    tag: StrictStr = Field(description="Tag name for this outbound")
    type: StrictStr = Field(description="Type of outbound protocol")
    server: StrictStr = Field(description="Server address")
    server_port: StrictInt = Field(description="Server port number")
    password: Optional[StrictStr] = Field(default=None, description="Authentication password")
    security: Optional[StrictStr] = Field(default=None, description="Security protocol")
    domain_resolver: Optional[StrictStr] = Field(default=None, description="Domain resolver configuration")
    full_config: Dict[str, Any] = Field(description="Complete configuration in JSON format")
    __properties: ClassVar[List[str]] = ["tag", "type", "server", "server_port", "password", "security", "domain_resolver", "full_config"]

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
        """Create an instance of SbOutboundCreate from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SbOutboundCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in SbOutboundCreate) in the input: " + _key)

        _obj = cls.model_validate({
            "tag": obj.get("tag"),
            "type": obj.get("type"),
            "server": obj.get("server"),
            "server_port": obj.get("server_port"),
            "password": obj.get("password"),
            "security": obj.get("security"),
            "domain_resolver": obj.get("domain_resolver"),
            "full_config": obj.get("full_config")
        })
        return _obj


