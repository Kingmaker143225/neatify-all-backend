from typing import Dict

from pydantic import BaseModel


class AvailabilitySaveRequest(BaseModel):
    month: str
    calendar_data: Dict[str, str]