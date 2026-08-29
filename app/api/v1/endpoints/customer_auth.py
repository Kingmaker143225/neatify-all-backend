# from fastapi import APIRouter, Depends

# from app.dependencies.customer_auth import (
#     get_current_customer,
# )

# from app.schemas.customer_auth import (
#     CustomerLoginRequest,
#     CustomerLoginResponse,
#     CustomerMeResponse,
#     CustomerLogoutResponse,
# )

# from app.services.customer_auth_service import (
#     CustomerAuthService,
# )


# router = APIRouter()


# # =========================================================
# # CUSTOMER LOGIN
# # =========================================================

# @router.post(
#     "/login",
#     response_model=CustomerLoginResponse,
# )
# async def customer_login(
#     request: CustomerLoginRequest,
# ):
#     return CustomerAuthService.login(
#         email=request.email,
#         password=request.password,
#     )


# # =========================================================
# # CUSTOMER ME
# # =========================================================

# @router.get(
#     "/me",
#     response_model=CustomerMeResponse,
# )
# async def customer_me(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return CustomerAuthService.get_me(
#         access_token=current_customer[
#             "access_token"
#         ],
#     )


# # =========================================================
# # CUSTOMER LOGOUT
# # =========================================================

# @router.post(
#     "/logout",
#     response_model=CustomerLogoutResponse,
# )
# async def customer_logout(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return CustomerAuthService.logout(
#         access_token=current_customer[
#             "access_token"
#         ],
#     )














# from fastapi import APIRouter, Depends

# from app.dependencies.customer_auth import (
#     get_current_customer,
# )

# from app.schemas.customer_auth import (
#     CustomerLoginRequest,
#     CustomerLoginResponse,
#     CustomerSignupRequest,
#     CustomerSignupResponse,
#     CustomerMeResponse,
#     CustomerProfileCompletenessResponse,
#     CustomerSendOtpRequest,
#     CustomerSendOtpResponse,
#     CustomerVerifyOtpRequest,
#     CustomerVerifyOtpResponse,
#     CustomerLogoutResponse,
# )

# from app.services.customer_auth_service import (
#     CustomerAuthService,
# )


# router = APIRouter()


# # =========================================================
# # CUSTOMER LOGIN
# # =========================================================

# @router.post(
#     "/login",
#     response_model=CustomerLoginResponse,
# )
# async def customer_login(
#     request: CustomerLoginRequest,
# ):
#     return CustomerAuthService.login(
#         email=request.email,
#         password=request.password,
#     )


# # =========================================================
# # CUSTOMER SIGNUP
# # =========================================================

# @router.post(
#     "/signup",
#     response_model=CustomerSignupResponse,
# )
# async def customer_signup(
#     request: CustomerSignupRequest,
# ):
#     return CustomerAuthService.signup(
#         full_name=request.full_name,
#         email=request.email,
#         phone=request.phone,
#         password=request.password,
#     )


# # =========================================================
# # CURRENT CUSTOMER
# # =========================================================

# @router.get(
#     "/me",
#     response_model=CustomerMeResponse,
# )
# async def customer_me(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return CustomerAuthService.get_me(
#         access_token=current_customer[
#             "access_token"
#         ],
#     )


# # =========================================================
# # CUSTOMER PROFILE COMPLETENESS
# # =========================================================

# @router.get(
#     "/profile-completeness",
#     response_model=CustomerProfileCompletenessResponse,
# )
# async def customer_profile_completeness(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return (
#         CustomerAuthService
#         .get_profile_completeness(
#             access_token=current_customer[
#                 "access_token"
#             ],
#         )
#     )


# # =========================================================
# # SEND CUSTOMER OTP
# # =========================================================

# @router.post(
#     "/send-otp",
#     response_model=CustomerSendOtpResponse,
# )
# async def customer_send_otp(
#     request: CustomerSendOtpRequest,
# ):
#     return CustomerAuthService.send_otp(
#         phone=request.phone,
#     )


# # =========================================================
# # VERIFY CUSTOMER OTP
# # =========================================================

# @router.post(
#     "/verify-otp",
#     response_model=CustomerVerifyOtpResponse,
# )
# async def customer_verify_otp(
#     request: CustomerVerifyOtpRequest,
# ):
#     return CustomerAuthService.verify_otp(
#         phone=request.phone,
#         otp=request.otp,
#     )


# # =========================================================
# # CUSTOMER LOGOUT
# # =========================================================

# @router.post(
#     "/logout",
#     response_model=CustomerLogoutResponse,
# )
# async def customer_logout(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return CustomerAuthService.logout(
#         access_token=current_customer[
#             "access_token"
#         ],
#     )






















from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_auth import (
    CustomerLoginRequest,
    CustomerLoginResponse,
    CustomerSignupRequest,
    CustomerSignupResponse,
    CustomerMeResponse,
    CustomerProfileCompletenessResponse,
    CustomerSendOtpRequest,
    CustomerSendOtpResponse,
    CustomerVerifyOtpRequest,
    CustomerVerifyOtpResponse,
    CustomerLogoutResponse,
    CustomerRewardsResponse,
    CustomerRewardsUpdateRequest,
)

from app.services.customer_auth_service import (
    CustomerAuthService,
)


router = APIRouter()


# =========================================================
# CUSTOMER LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=CustomerLoginResponse,
)
async def customer_login(
    request: CustomerLoginRequest,
):
    return CustomerAuthService.login(
        email=request.email,
        password=request.password,
    )


# =========================================================
# CUSTOMER SIGNUP
# =========================================================

@router.post(
    "/signup",
    response_model=CustomerSignupResponse,
)
async def customer_signup(
    request: CustomerSignupRequest,
):
    return CustomerAuthService.signup(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password=request.password,
    )


# =========================================================
# CURRENT CUSTOMER
# =========================================================

@router.get(
    "/me",
    response_model=CustomerMeResponse,
)
async def customer_me(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerAuthService.get_me(
        access_token=current_customer[
            "access_token"
        ],
    )


# =========================================================
# CUSTOMER PROFILE COMPLETENESS
# =========================================================

@router.get(
    "/profile-completeness",
    response_model=CustomerProfileCompletenessResponse,
)
async def customer_profile_completeness(
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerAuthService
        .get_profile_completeness(
            access_token=current_customer[
                "access_token"
            ],
        )
    )


# =========================================================
# CUSTOMER REWARDS / OFFERS
# =========================================================

@router.get(
    "/rewards",
    response_model=CustomerRewardsResponse,
)
async def customer_rewards(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerAuthService.get_rewards(
        access_token=current_customer[
            "access_token"
        ],
    )


@router.patch(
    "/rewards",
    response_model=CustomerRewardsResponse,
)
async def update_customer_rewards(
    request: CustomerRewardsUpdateRequest,
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerAuthService.update_rewards(
        access_token=current_customer[
            "access_token"
        ],
        show_welcome_reward=request.show_welcome_reward,
        show_signup_offer_popup=request.show_signup_offer_popup,
    )


# =========================================================
# SEND CUSTOMER OTP
# =========================================================

@router.post(
    "/send-otp",
    response_model=CustomerSendOtpResponse,
)
async def customer_send_otp(
    request: CustomerSendOtpRequest,
):
    return CustomerAuthService.send_otp(
        phone=request.phone,
    )


# =========================================================
# VERIFY CUSTOMER OTP
# =========================================================

@router.post(
    "/verify-otp",
    response_model=CustomerVerifyOtpResponse,
)
async def customer_verify_otp(
    request: CustomerVerifyOtpRequest,
):
    return CustomerAuthService.verify_otp(
        phone=request.phone,
        otp=request.otp,
    )


# =========================================================
# CUSTOMER LOGOUT
# =========================================================

@router.post(
    "/logout",
    response_model=CustomerLogoutResponse,
)
async def customer_logout(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerAuthService.logout(
        access_token=current_customer[
            "access_token"
        ],
    )