from pydantic import BaseModel, Field


class CustomerCartItemAddRequest(BaseModel):
    service_id: str = Field(
        ...,
        min_length=1,
    )


class CustomerCartItemResponse(BaseModel):
    id: str
    service_id: str
    title: str
    duration: str | None = None
    price: str
    image: str | None = None
    created_at: str | None = None


class CustomerCartResponse(BaseModel):
    success: bool
    items: list[CustomerCartItemResponse]
    message: str