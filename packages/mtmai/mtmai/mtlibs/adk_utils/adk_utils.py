from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


def tool_success(data: dict[str, Any] | str | BaseModel | None):
    if data is None:
        return {
            "success": False,
        }
    if isinstance(data, BaseModel):
        return {
            "success": True,
            "result": jsonable_encoder(data.model_dump()),
        }
    if isinstance(data, str):
        return {
            "success": True,
            "result": data,
        }
    return {
        "success": True,
        "result": data,
    }
