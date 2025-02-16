import asyncio
import base64
import json
import traceback
from typing import Any

import grpc
import tenacity
from loguru import logger


def tenacity_retry(func):
    return tenacity.retry(
        reraise=True,
        wait=tenacity.wait_exponential_jitter(),
        stop=tenacity.stop_after_attempt(5),
        before_sleep=tenacity_alert_retry,
        retry=tenacity.retry_if_exception(tenacity_should_retry),
    )(func)


def tenacity_alert_retry(retry_state: tenacity.RetryCallState) -> None:
    """Called between tenacity retries."""
    logger.debug(
        f"Retrying {retry_state.fn}: attempt "
        f"{retry_state.attempt_number} ended with: {retry_state.outcome}",
    )


def tenacity_should_retry(ex: Exception) -> bool:
    if isinstance(ex, grpc.aio.AioRpcError):
        if ex.code in [
            grpc.StatusCode.UNIMPLEMENTED,
            grpc.StatusCode.NOT_FOUND,
        ]:
            return False
        return True
    else:
        return False


def get_metadata(token: str):
    return [("authorization", "bearer " + token)]


class Event_ts(asyncio.Event):
    """
    Event_ts is a subclass of asyncio.Event that allows for thread-safe setting and clearing of the event.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

    def set(self):
        if not self._loop.is_closed():
            self._loop.call_soon_threadsafe(super().set)

    def clear(self):
        self._loop.call_soon_threadsafe(super().clear)


async def read_with_interrupt(listener: Any, interrupt: Event_ts):
    try:
        result = await listener.read()
        return result
    finally:
        interrupt.set()


def get_tenant_id_from_jwt(token: str) -> str:
    claims = extract_claims_from_jwt(token)

    return claims.get("sub")


def get_addresses_from_jwt(token: str) -> (str, str):
    claims = extract_claims_from_jwt(token)

    return claims.get("server_url"), claims.get("grpc_broadcast_address")


def extract_claims_from_jwt(token: str):
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    claims_part = parts[1]
    claims_part += "=" * ((4 - len(claims_part) % 4) % 4)  # Padding for base64 decoding
    claims_data = base64.urlsafe_b64decode(claims_part)
    claims = json.loads(claims_data)

    return claims


def errorWithTraceback(message: str, e: Exception):
    trace = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    return f"{message}\n{trace}"
