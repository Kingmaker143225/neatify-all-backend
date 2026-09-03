from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    id: str
    email: str
    terms_accepted: bool = False
    privacy_policy_accepted: bool = False


class LogoutResponse(BaseModel):
    success: bool
    message: str