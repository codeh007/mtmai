from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

# from mtmai.chainlit.config import config
# from mtmai.chainlit.oauth_providers import get_configured_oauth_providers
from mtmai.core import security
from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmai.crud import curd
from mtmai.deps import get_asession
from mtmai.models.models import TokenPayload, User

logger = get_logger()
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


def get_jwt_secret():
    return settings.SECRET_KEY


def ensure_jwt_secret():
    if require_login() and get_jwt_secret() is None:
        raise ValueError(
            "You must provide a JWT secret in the environment to use authentication. Run `chainlit create-secret` to generate one."
        )


def is_oauth_enabled():
    return config.code.oauth_callback and len(get_configured_oauth_providers()) > 0


def require_login():
    return True


# def get_configuration():
#     return {
#         "requireLogin": require_login(),
#         "passwordAuth": config.code.password_auth_callback is not None,
#         "headerAuth": config.code.header_auth_callback is not None,
#         "oauthProviders": get_configured_oauth_providers()
#         if is_oauth_enabled()
#         else [],
# }


def create_jwt(data: User) -> str:
    to_encode = data.to_dict()
    to_encode.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=60 * 24 * 15),  # 15 days
        }
    )
    encoded_jwt = jwt.encode(to_encode, get_jwt_secret(), algorithm="HS256")
    return encoded_jwt


async def authenticate_user(
    token: str = Depends(reuseable_oauth), session=Depends(get_asession)
):
    try:
        logger.info(f"secret: {settings.SECRET_KEY}, token: {token}, ")
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # user = await session.get(User, token_data.sub)
    user = await curd.get_user_by_id(session=session, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_current_user(
    token: str = Depends(reuseable_oauth), session=Depends(get_asession)
):
    if not require_login():
        return None
    logger.info(f"call get_current_user token: {token}")
    return await authenticate_user(token, session=session)
