from pydantic import BaseModel


class InstagramAccountState(BaseModel):
    """
    Represents a customer's address.
    """

    name: str | None = None
    ig_settings: dict | None = None
