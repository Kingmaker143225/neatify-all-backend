from pydantic import BaseModel, Field


class CustomerProfileResponse(BaseModel):
    id: str
    full_name: str | None = None
    email: str
    phone: str | None = None
    address: str | None = None
    pincode: str | None = None
    referral_code : str | None  = None


class CustomerProfileUpdateRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    phone: str
    address: str = ""
    pincode: str = ""

class CustomerCompleteProfileRequest(BaseModel):

    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    email: str

    phone: str

    password: str | None = None

    referral_code: str | None = None