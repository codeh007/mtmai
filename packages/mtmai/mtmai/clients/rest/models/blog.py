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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from mtmai.clients.rest.models.api_resource_meta import APIResourceMeta
from mtmai.clients.rest.models.blog_config import BlogConfig
from mtmai.clients.rest.models.tenant import Tenant
from typing import Optional, Set
from typing_extensions import Self

class Blog(BaseModel):
    """
    Blog
    """ # noqa: E501
    metadata: APIResourceMeta
    title: StrictStr
    description: Optional[StrictStr] = None
    tenant: Optional[Tenant] = Field(default=None, description="The tenant associated with this tenant blog.")
    config: Optional[BlogConfig] = None
    status: Optional[StrictStr] = Field(default=None, description="The status of the blog.")
    enabled: Optional[StrictBool] = Field(default=None, description="Whether the blog is enabled.")
    slug: Optional[StrictStr] = Field(default=None, description="The slug of the blog.")
    __properties: ClassVar[List[str]] = ["metadata", "title", "description", "tenant", "config", "status", "enabled", "slug"]

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
        """Create an instance of Blog from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of tenant
        if self.tenant:
            _dict['tenant'] = self.tenant.to_dict()
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict['config'] = self.config.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Blog from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in Blog) in the input: " + _key)

        _obj = cls.model_validate({
            "metadata": APIResourceMeta.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "title": obj.get("title"),
            "description": obj.get("description"),
            "tenant": Tenant.from_dict(obj["tenant"]) if obj.get("tenant") is not None else None,
            "config": BlogConfig.from_dict(obj["config"]) if obj.get("config") is not None else None,
            "status": obj.get("status"),
            "enabled": obj.get("enabled"),
            "slug": obj.get("slug")
        })
        return _obj


