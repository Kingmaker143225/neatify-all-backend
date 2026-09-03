from pydantic import BaseModel


class AdminProfileResponse(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str
    address: str
    pincode: str


class AdminProfileUpdateRequest(BaseModel):
    full_name: str
    phone: str
    address: str
    pincode: str