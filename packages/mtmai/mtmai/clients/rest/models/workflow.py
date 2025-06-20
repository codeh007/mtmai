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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from mtmai.clients.rest.models.api_resource_meta import APIResourceMeta
from mtmai.clients.rest.models.job import Job
from mtmai.clients.rest.models.workflow_tag import WorkflowTag
from typing import Optional, Set
from typing_extensions import Self

class Workflow(BaseModel):
    """
    Workflow
    """ # noqa: E501
    metadata: APIResourceMeta
    name: StrictStr = Field(description="The name of the workflow.")
    description: Optional[StrictStr] = Field(default=None, description="The description of the workflow.")
    is_paused: Optional[StrictBool] = Field(default=None, description="Whether the workflow is paused.", alias="isPaused")
    versions: Optional[List[WorkflowVersionMeta]] = None
    tags: Optional[List[WorkflowTag]] = Field(default=None, description="The tags of the workflow.")
    jobs: Optional[List[Job]] = Field(default=None, description="The jobs of the workflow.")
    tenant_id: StrictStr = Field(description="The tenant id of the workflow.", alias="tenantId")
    __properties: ClassVar[List[str]] = ["metadata", "name", "description", "isPaused", "versions", "tags", "jobs", "tenantId"]

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
        """Create an instance of Workflow from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in versions (list)
        _items = []
        if self.versions:
            for _item_versions in self.versions:
                if _item_versions:
                    _items.append(_item_versions.to_dict())
            _dict['versions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item_tags in self.tags:
                if _item_tags:
                    _items.append(_item_tags.to_dict())
            _dict['tags'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in jobs (list)
        _items = []
        if self.jobs:
            for _item_jobs in self.jobs:
                if _item_jobs:
                    _items.append(_item_jobs.to_dict())
            _dict['jobs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Workflow from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in Workflow) in the input: " + _key)

        _obj = cls.model_validate({
            "metadata": APIResourceMeta.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "name": obj.get("name"),
            "description": obj.get("description"),
            "isPaused": obj.get("isPaused"),
            "versions": [WorkflowVersionMeta.from_dict(_item) for _item in obj["versions"]] if obj.get("versions") is not None else None,
            "tags": [WorkflowTag.from_dict(_item) for _item in obj["tags"]] if obj.get("tags") is not None else None,
            "jobs": [Job.from_dict(_item) for _item in obj["jobs"]] if obj.get("jobs") is not None else None,
            "tenantId": obj.get("tenantId")
        })
        return _obj

from mtmai.clients.rest.models.workflow_version_meta import WorkflowVersionMeta
# TODO: Rewrite to not use raise_errors
Workflow.model_rebuild(raise_errors=False)

