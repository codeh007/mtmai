from typing import Literal

from camelCasing import camelCasing
from pydantic import BaseModel, Field

registered_forms: dict[str, type[BaseModel]] = {}


def get_form_by_name(name: str) -> type[BaseModel]:
    return registered_forms.get(name)


def mtform(name: str | None = None):
    """
    表单装饰器，用于注册表单并设置表单属性
    """

    def decorator(cls: type[BaseModel]):
        nonlocal name
        if name is None:
            name = camelCasing.toCamelCase(cls.__name__)
        if name in registered_forms:
            msg = f"Form with name '{name}' already exists"
            raise ValueError(msg)
        registered_forms[name] = cls
        return cls

    return decorator


class FormFieldSchema(BaseModel):
    name: str
    placeholder: str | None = None
    valueType: str | None = None
    defaultValue: str | None = None
    description: str | None = None
    label: str | None = None
    type: str | None = None


class MtForm(BaseModel):
    properties: dict[str, FormFieldSchema]
    title: str
    type: str = Field(default="object")
    variant: Literal["default"] = Field(default="default")

    class Config:  # noqa: D106
        arbitrary_types_allowed = True
