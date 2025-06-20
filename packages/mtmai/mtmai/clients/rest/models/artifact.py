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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBytes, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class Artifact(BaseModel):
    """
    Artifact
    """ # noqa: E501
    id: Annotated[str, Field(min_length=36, strict=True, max_length=36)] = Field(description="The artifact id.")
    created_at: datetime = Field(description="The artifact created at.")
    updated_at: StrictStr = Field(description="The artifact updated at.")
    tenant_id: Annotated[str, Field(min_length=36, strict=True, max_length=36)] = Field(description="The artifact tenant id.")
    user_id: StrictStr
    version: StrictInt
    session_id: StrictStr
    app_name: StrictStr
    filename: StrictStr
    mime_type: Optional[StrictStr] = None
    content: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]] = Field(description="The artifact content.")
    __properties: ClassVar[List[str]] = ["id", "created_at", "updated_at", "tenant_id", "user_id", "version", "session_id", "app_name", "filename", "mime_type", "content"]

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
        """Create an instance of Artifact from a JSON string"""
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
        """Create an instance of Artifact from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in Artifact) in the input: " + _key)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "tenant_id": obj.get("tenant_id"),
            "user_id": obj.get("user_id"),
            "version": obj.get("version"),
            "session_id": obj.get("session_id"),
            "app_name": obj.get("app_name"),
            "filename": obj.get("filename"),
            "mime_type": obj.get("mime_type"),
            "content": obj.get("content")
        })
        return _obj


