from contextvars import ContextVar

from mtmai.models.models import User

user_id_context: ContextVar[str] = ContextVar("user_id", default=None)
user_context: ContextVar[User] = ContextVar("user", default=None)


def get_current_user_id() -> str:
    return user_id_context.get()


def set_current_user_id(user_id: str):
    user_id_context.set(user_id)


def get_user() -> User | None:
    return user_context.get()


def set_user(user: User):
    user_context.set(user)


project_id_context: ContextVar[str] = ContextVar("project_id", default=None)
project_context: ContextVar[User] = ContextVar("project", default=None)
