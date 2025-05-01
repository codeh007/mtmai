import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, TypeVar, cast

import jwt
from google.protobuf.message import Message
from jinja2 import Template
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from mtmai.core.config import settings


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a given filename by replacing characters that are invalid
    in Windows file paths with an underscore ('_').

    This function ensures that the filename is compatible with all
    operating systems by removing or replacing characters that are
    not allowed in Windows file paths. Specifically, it replaces
    the following characters: < > : " / \ | ? *

    Parameters:
    filename (str): The original filename to be sanitized.

    Returns:
    str: The sanitized filename with invalid characters replaced by an underscore.

    Examples:
    >>> sanitize_filename('invalid:file/name*example?.txt')
    'invalid_file_name_example_.txt'

    >>> sanitize_filename('valid_filename.txt')
    'valid_filename.txt'
    """
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


# def send_email(
#     *,
#     email_to: str,
#     subject: str = "",
#     html_content: str = "",
# ) -> None:
#     # assert settings.emails_enabled, "no provided configuration for email variables"
#     message = emails.Message(
#         subject=subject,
#         html=html_content,
#         mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
#     )
#     smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     elif settings.SMTP_SSL:
#         smtp_options["ssl"] = True
#     if settings.SMTP_USER:
#         smtp_options["user"] = settings.SMTP_USER
#     if settings.SMTP_PASSWORD:
#         smtp_options["password"] = settings.SMTP_PASSWORD
#     response = message.send(to=email_to, smtp=smtp_options)
#     logging.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None


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


def http_url_ws(url: str) -> str:
    if url.startswith("http"):
        return url.replace("http", "ws")
    elif url.startswith("https"):
        return url.replace("https", "wss")
    else:
        raise ValueError(f"Invalid URL: {url}")


# def run_async_function(func: Callable, *args: Any, **kwargs: Any) -> Any:
#     """
#     运行一个异步函数，并返回其结果。

#     Args:
#         func: 要运行的异步函数。
#         *args: 传递给异步函数的参数。
#         **kwargs: 传递给异步函数的关键字参数。

#     Returns:
#         Any: 异步函数的返回值。
#     """
#     loop = asyncio.get_event_loop()
#     # if loop.is_running():
#     #     loop = asyncio.new_event_loop()
#     #     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(func(*args, **kwargs))
