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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class AssignedAction(BaseModel):
    """
    AssignedAction
    """ # noqa: E501
    tenant_id: StrictStr = Field(alias="tenantId")
    workflow_run_id: Optional[StrictStr] = Field(default=None, alias="workflowRunId")
    get_group_key_run_id: Optional[StrictStr] = Field(default=None, alias="getGroupKeyRunId")
    job_id: StrictStr = Field(alias="jobId")
    job_name: Optional[StrictStr] = Field(default=None, alias="jobName")
    step_id: StrictStr = Field(alias="stepId")
    step_run_id: Optional[StrictStr] = Field(default=None, alias="stepRunId")
    action_id: StrictStr = Field(alias="actionId")
    action_type: StrictStr = Field(alias="actionType")
    action_payload: StrictStr = Field(alias="actionPayload")
    step_name: StrictStr = Field(alias="stepName")
    retry_count: StrictInt = Field(alias="retryCount")
    additional_metadata: Optional[StrictStr] = None
    child_workflow_index: Optional[StrictInt] = None
    child_workflow_key: Optional[StrictStr] = None
    parent_workflow_run_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["tenantId", "workflowRunId", "getGroupKeyRunId", "jobId", "jobName", "stepId", "stepRunId", "actionId", "actionType", "actionPayload", "stepName", "retryCount", "additional_metadata", "child_workflow_index", "child_workflow_key", "parent_workflow_run_id"]

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
        """Create an instance of AssignedAction from a JSON string"""
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
        """Create an instance of AssignedAction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in AssignedAction) in the input: " + _key)

        _obj = cls.model_validate({
            "tenantId": obj.get("tenantId"),
            "workflowRunId": obj.get("workflowRunId"),
            "getGroupKeyRunId": obj.get("getGroupKeyRunId"),
            "jobId": obj.get("jobId"),
            "jobName": obj.get("jobName"),
            "stepId": obj.get("stepId"),
            "stepRunId": obj.get("stepRunId"),
            "actionId": obj.get("actionId"),
            "actionType": obj.get("actionType"),
            "actionPayload": obj.get("actionPayload"),
            "stepName": obj.get("stepName"),
            "retryCount": obj.get("retryCount"),
            "additional_metadata": obj.get("additional_metadata"),
            "child_workflow_index": obj.get("child_workflow_index"),
            "child_workflow_key": obj.get("child_workflow_key"),
            "parent_workflow_run_id": obj.get("parent_workflow_run_id")
        })
        return _obj


