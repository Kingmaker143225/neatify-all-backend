# from pydantic import BaseModel, EmailStr


# class CustomerLoginRequest(BaseModel):
#     email: EmailStr
#     password: str


# class CustomerLoginResponse(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
#     user_id: str
#     email: str
#     profile_exists: bool


# class CustomerProfileSummary(BaseModel):
#     id: str
#     full_name: str | None = None
#     email: str | None = None
#     phone: str | None = None


# class CustomerMeResponse(BaseModel):
#     id: str
#     email: str
#     profile_exists: bool
#     profile: CustomerProfileSummary | None = None


# class CustomerLogoutResponse(BaseModel):
#     success: bool
#     message: str
















from pydantic import BaseModel, EmailStr, Field


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


class CustomerSignupRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    email: EmailStr
    phone: str
    password: str = Field(
        ...,
        min_length=6,
    )


class CustomerSignupResponse(BaseModel):
    user_id: str
    email: str
    profile_created: bool
    email_confirmation_required: bool
    message: str


class CustomerProfileSummary(BaseModel):
    id: str
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None


class CustomerMeResponse(BaseModel):
    id: str
    email: str
    email_confirmed: bool
    profile_exists: bool
    profile_complete: bool
    profile: CustomerProfileSummary | None = None


class CustomerProfileCompletenessResponse(BaseModel):
    profile_exists: bool
    profile_complete: bool
    email_confirmed: bool
    missing_fields: list[str]


class CustomerSendOtpRequest(BaseModel):
    phone: str


class CustomerSendOtpResponse(BaseModel):
    success: bool
    message: str


class CustomerVerifyOtpRequest(BaseModel):
    phone: str
    otp: str


class CustomerVerifyOtpResponse(BaseModel):
    success: bool
    is_new_user: bool
    email: str | None = None
    temp_password: str | None = None
    message: str


class CustomerLogoutResponse(BaseModel):
    success: bool
    message: str