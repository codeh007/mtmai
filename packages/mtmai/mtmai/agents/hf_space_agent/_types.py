from pydantic import BaseModel


class ResetHFMsg(BaseModel):
    username: str
    space: str
    token: str
