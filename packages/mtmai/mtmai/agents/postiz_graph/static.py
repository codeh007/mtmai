from pydantic import BaseModel, Field


class Topic(BaseModel):
    topic: str = Field(description="The topic for the post")
