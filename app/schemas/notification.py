from typing import Any

from pydantic import BaseModel, Field


class SendStaffNotificationRequest(BaseModel):
    token: str = Field(..., min_length=1)
    title: str | None = None
    body: str | None = None
    data: dict[str, Any] | None = None


class StaffNotificationRequest(BaseModel):
    email: str = Field(..., min_length=1)
    title: str | None = None
    body: str | None = None
    data: dict[str, Any] | None = None