import jwt
from pydantic import ValidationError

from mtmai.core import security
from mtmai.core.config import settings
from mtmai.models.models import TokenPayload


class TokenDecodeError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return TokenPayload(**payload)
    except jwt.InvalidTokenError:
        raise TokenDecodeError("Invalid token")
    except jwt.ExpiredSignatureError:
        raise TokenDecodeError("Token has expired")
    except jwt.DecodeError:
        raise TokenDecodeError("Could not decode token")
    except ValidationError:
        raise TokenDecodeError("Invalid token payload")
