import jwt
from fastapi import Request
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from mtmai.context import set_current_user_id, set_user
from mtmai.core import security
from mtmai.core.config import settings
from mtmai.crud import curd
from mtmai.models.models import TokenPayload


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        jwt_token = None
        authorization = request.headers.get("Authorization")
        if authorization:
            jwt_token = authorization[7:]  # bearer
        if not jwt_token:
            if settings.COOKIE_ACCESS_TOKEN:
                jwt_token = request.cookies.get(settings.COOKIE_ACCESS_TOKEN)

        if not jwt_token:
            return await call_next(request)
        try:
            payload = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            set_current_user_id(token_data.sub)
        except (InvalidTokenError, ValidationError):
            return await call_next(request)
        user = await curd.get_user_by_id(token_data.sub)
        if user:
            set_user(user)

        return await call_next(request)
