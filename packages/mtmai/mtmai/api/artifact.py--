from typing import Annotated
from urllib.parse import unquote

import structlog
from fastapi import APIRouter, HTTPException, Query, Request, Response

from mtmai.deps import OptionalUserDep

router = APIRouter()

LOG = structlog.get_logger()


@router.get("/image")
async def get_thread_element(
    request: Request,
    user: OptionalUserDep,
    path: Annotated[str | None, Query()] = None,
):
    """获取图像的artifact"""
    if not path:
        raise HTTPException(
            status_code=400,
            detail=f"Path parameter is required (received: {path}, query_params: {dict(request.query_params)})",
        )

    file_path = unquote(path)

    try:
        with open(file_path, "rb") as f:
            image_data = f.read()
        # Add required CORS and security headers
        headers = {
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Resource-Policy": "cross-origin",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }

        return Response(content=image_data, media_type="image/png", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
