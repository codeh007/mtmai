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

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from mtmai.clients.rest.models.form_field import FormField
from typing import Optional, Set
from typing_extensions import Self

class SchemaForm(BaseModel):
    """
    SchemaForm
    """ # noqa: E501
    form_type: Optional[StrictStr] = 'schema'
    form_name: Optional[StrictStr] = None
    title: StrictStr
    description: Optional[StrictStr] = None
    layout: Optional[StrictStr] = 'vertical'
    fields: List[FormField]
    __properties: ClassVar[List[str]] = ["form_type", "form_name", "title", "description", "layout", "fields"]

    @field_validator('form_type')
    def form_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['schema', 'custom']):
            raise ValueError("must be one of enum values ('schema', 'custom')")
        return value

    @field_validator('layout')
    def layout_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['vertical', 'horizontal']):
            raise ValueError("must be one of enum values ('vertical', 'horizontal')")
        return value

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
        """Create an instance of SchemaForm from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in fields (list)
        _items = []
        if self.fields:
            for _item_fields in self.fields:
                if _item_fields:
                    _items.append(_item_fields.to_dict())
            _dict['fields'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SchemaForm from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in SchemaForm) in the input: " + _key)

        _obj = cls.model_validate({
            "form_type": obj.get("form_type") if obj.get("form_type") is not None else 'schema',
            "form_name": obj.get("form_name"),
            "title": obj.get("title"),
            "description": obj.get("description"),
            "layout": obj.get("layout") if obj.get("layout") is not None else 'vertical',
            "fields": [FormField.from_dict(_item) for _item in obj["fields"]] if obj.get("fields") is not None else None
        })
        return _obj


