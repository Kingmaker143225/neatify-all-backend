from pydantic import BaseModel, EmailStr


class CustomerLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CustomerLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    profile_exists: bool


class CustomerProfileSummary(BaseModel):
    id: str
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None


class CustomerMeResponse(BaseModel):
    id: str
    email: str
    profile_exists: bool
    profile: CustomerProfileSummary | None = None


class CustomerLogoutResponse(BaseModel):
    success: bool
    message: str