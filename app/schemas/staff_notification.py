from pydantic import BaseModel


class StaffNotificationRequest(BaseModel):
    email: str
    title: str | None = None
    body: str | None = None