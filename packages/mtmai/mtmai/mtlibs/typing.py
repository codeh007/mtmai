from typing import Any, TypeVar, cast

from google.protobuf.message import Message
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def is_basemodel_subclass(model: Any) -> bool:
    try:
        return issubclass(model, BaseModel)
    except TypeError:
        return False


def get_type_name(cls: type[Any] | Any) -> str:
    # If cls is a protobuf, then we need to determine the descriptor
    if isinstance(cls, type):
        if issubclass(cls, Message):
            return cast(str, cls.DESCRIPTOR.full_name)
    elif isinstance(cls, Message):
        return cast(str, cls.DESCRIPTOR.full_name)

    if isinstance(cls, type):
        return cls.__name__
    else:
        return cast(str, cls.__class__.__name__)
