from pydantic import BaseModel, Field


class CustomerPushTokenRequest(BaseModel):
    token: str = Field(
        ...,
        min_length=1,
    )
    platform: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )