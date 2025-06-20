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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class PlatformCreate(BaseModel):
    """
    PlatformCreate
    """ # noqa: E501
    id: StrictStr = Field(description="UUID of the platform")
    name: StrictStr = Field(description="Name of the platform")
    url: Optional[StrictStr] = Field(default=None, description="URL of the platform")
    description: Optional[StrictStr] = Field(default=None, description="Description of the platform")
    login_url: Optional[StrictStr] = Field(default=None, description="Login URL for the platform", alias="loginUrl")
    tags: Optional[List[StrictStr]] = Field(default=None, description="Tags for categorizing the platform")
    __properties: ClassVar[List[str]] = ["id", "name", "url", "description", "loginUrl", "tags"]

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
        """Create an instance of PlatformCreate from a JSON string"""
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
        """Create an instance of PlatformCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in PlatformCreate) in the input: " + _key)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "url": obj.get("url"),
            "description": obj.get("description"),
            "loginUrl": obj.get("loginUrl"),
            "tags": obj.get("tags")
        })
        return _obj


