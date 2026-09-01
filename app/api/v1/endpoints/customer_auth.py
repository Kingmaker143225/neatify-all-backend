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
#     CustomerRewardsResponse,
#     CustomerRewardsUpdateRequest,
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
# # CUSTOMER REWARDS / OFFERS
# # =========================================================

# @router.get(
#     "/rewards",
#     response_model=CustomerRewardsResponse,
# )
# async def customer_rewards(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return CustomerAuthService.get_rewards(
#         access_token=current_customer[
#             "access_token"
#         ],
#     )


# @router.patch(
#     "/rewards",
#     response_model=CustomerRewardsResponse,
# )
# async def update_customer_rewards(
#     request: CustomerRewardsUpdateRequest,
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     return CustomerAuthService.update_rewards(
#         access_token=current_customer[
#             "access_token"
#         ],
#         show_welcome_reward=request.show_welcome_reward,
#         show_signup_offer_popup=request.show_signup_offer_popup,
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

















from fastapi import APIRouter, Depends, HTTPException

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
    # ✅ Google OAuth schemas
    CustomerGoogleOAuthUrlRequest,
    CustomerGoogleOAuthUrlResponse,
    CustomerGoogleExchangeRequest,
    CustomerGoogleExchangeResponse,
)

from app.services.customer_auth_service import (
    CustomerAuthService,
)

# ✅ Import for Google OAuth
from app.supabase.client import supabase
from app.repositories.customer_repository import CustomerRepository


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


# =========================================================
# ✅ GOOGLE OAUTH - GET OAUTH URL
# =========================================================

@router.post(
    "/google/oauth-url",
    response_model=CustomerGoogleOAuthUrlResponse,
)
async def get_google_oauth_url(
    request: CustomerGoogleOAuthUrlRequest,
):
    """
    Get Google OAuth URL for initiating the sign-in flow.
    
    This endpoint uses Supabase's OAuth capabilities but
    returns the URL to the frontend for browser navigation.
    """
    try:
        print(f"🔐 [GoogleAuth] Generating OAuth URL for redirect: {request.redirect_to}")
        
        # ✅ Use Supabase for OAuth URL generation
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirectTo": request.redirect_to,
            },
        })
        
        oauth_url = None
        
        if hasattr(response, 'data'):
            data = response.data
            if hasattr(data, 'url'):
                oauth_url = data.url
            elif isinstance(data, dict):
                oauth_url = data.get('url')
        elif hasattr(response, 'url'):
            oauth_url = response.url
        elif isinstance(response, dict):
            oauth_url = response.get('data', {}).get('url') or response.get('url')
        
        if not oauth_url:
            print(f"❌ [GoogleAuth] Could not extract URL from response: {response}")
            raise HTTPException(
                status_code=400,
                detail="No OAuth URL returned from Supabase"
            )
        
        print(f"✅ [GoogleAuth] OAuth URL generated successfully")
        
        return CustomerGoogleOAuthUrlResponse(
            oauth_url=oauth_url,
            provider="google"
        )
        
    except Exception as e:
        print(f"❌ [GoogleAuth] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate OAuth URL: {str(e)}"
        )


# =========================================================
# ✅ GOOGLE OAUTH - EXCHANGE CODE FOR TOKENS
# =========================================================

@router.post(
    "/google/exchange",
    response_model=CustomerGoogleExchangeResponse,
)
async def exchange_google_auth_code(
    request: CustomerGoogleExchangeRequest,
):
    """
    Exchange Google authorization code for user session and tokens.
    
    This endpoint:
    1. Exchanges the Google auth code for a Supabase session
    2. Gets user info from the session
    3. Creates/updates user in the database
    4. Returns a backend JWT token
    """
    try:
        print(f"🔐 [GoogleAuth] Exchanging auth code: {request.auth_code[:20]}...")
        
        # =========================================================
        # STEP 1: Exchange code for session using Supabase
        # =========================================================
        
        response = supabase.auth.exchange_code_for_session(
            request.auth_code
        )
        
        user = None
        session = None
        
        if hasattr(response, 'user'):
            user = response.user
        elif hasattr(response, 'data') and hasattr(response.data, 'user'):
            user = response.data.user
        elif isinstance(response, dict):
            user = response.get('user') or response.get('data', {}).get('user')
        
        if hasattr(response, 'session'):
            session = response.session
        elif hasattr(response, 'data') and hasattr(response.data, 'session'):
            session = response.data.session
        elif isinstance(response, dict):
            session = response.get('session') or response.get('data', {}).get('session')
        
        if not user:
            print(f"❌ [GoogleAuth] No user found in response: {response}")
            raise HTTPException(
                status_code=400,
                detail="No user found from OAuth exchange"
            )
        
        print(f"✅ [GoogleAuth] User authenticated: {user.email}")
        
        user_id = str(user.id)
        email = user.email or ""
        full_name = user.user_metadata.get("full_name", "") if hasattr(user, 'user_metadata') else ""
        
        # =========================================================
        # STEP 2: Check if profile exists
        # =========================================================
        
        profile = CustomerRepository.get_profile(user_id)
        profile_exists = profile is not None
        profile_complete = False
        
        if profile_exists:
            missing_fields = []
            if not profile.get("full_name"):
                missing_fields.append("full_name")
            if not profile.get("email"):
                missing_fields.append("email")
            if not profile.get("phone"):
                missing_fields.append("phone")
            
            profile_complete = len(missing_fields) == 0
        
        # =========================================================
        # STEP 3: Create user if they don't exist
        # =========================================================
        
        is_new_user = False
        if not profile_exists:
            is_new_user = True
            phone = user.user_metadata.get("phone", "") if hasattr(user, 'user_metadata') else ""
            CustomerRepository.upsert_profile(
                user_id=user_id,
                full_name=full_name or "",
                phone=phone,
                address="",
                pincode="",
                email=email,
            )
            print(f"✅ [GoogleAuth] Created new user profile: {user_id}")
        
        # =========================================================
        # STEP 4: Generate backend JWT token
        # =========================================================
        
        backend_token = CustomerAuthService._create_backend_token(user_id)
        
        print(f"✅ [GoogleAuth] Backend token generated")
        
        refresh_token = ""
        if session:
            if hasattr(session, 'refresh_token'):
                refresh_token = session.refresh_token
            elif isinstance(session, dict):
                refresh_token = session.get('refresh_token', '')
        
        return CustomerGoogleExchangeResponse(
            access_token=backend_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=user_id,
            email=email,
            full_name=full_name or None,
            profile_exists=profile_exists,
            profile_complete=profile_complete,
            is_new_user=is_new_user,
        )
        
    except Exception as e:
        print(f"❌ [GoogleAuth] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to exchange auth code: {str(e)}"
        )


# =========================================================
# ✅ CUSTOMER PASSWORD RESET (NEW)
# =========================================================

from pydantic import BaseModel  # Already imported at top of file


class ResetPasswordRequest(BaseModel):
    email: str
    redirect_to: str


class ResetPasswordConfirmRequest(BaseModel):
    access_token: str
    refresh_token: str
    new_password: str


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """
    Send password reset email to the user.
    """
    try:
        print(f"🔐 [PasswordReset] Sending reset email to: {request.email}")
        
        # ✅ Use Supabase to send reset email
        response = supabase.auth.reset_password_for_email(
            request.email,
            options={"redirectTo": request.redirect_to}
        )
        
        return {
            "success": True,
            "message": "Reset email sent successfully"
        }
        
    except Exception as e:
        print(f"❌ [PasswordReset] Error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to send reset email: {str(e)}"
        )


@router.post("/reset-password/confirm")
async def reset_password_confirm(request: ResetPasswordConfirmRequest):
    """
    Confirm password reset with new password using access/refresh tokens.
    """
    try:
        print(f"🔐 [PasswordReset] Confirming password reset...")
        
        # ✅ Set session with tokens
        response = supabase.auth.set_session(
            request.access_token,
            request.refresh_token
        )
        
        if not response.user:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired tokens"
            )
        
        # ✅ Update password
        update_response = supabase.auth.update_user({
            "password": request.new_password
        })
        
        if not update_response.user:
            raise HTTPException(
                status_code=400,
                detail="Failed to update password"
            )
        
        # ✅ Generate backend JWT token
        user_id = str(update_response.user.id)
        backend_token = CustomerAuthService._create_backend_token(user_id)
        
        return {
            "success": True,
            "message": "Password updated successfully",
            "access_token": backend_token
        }
        
    except Exception as e:
        print(f"❌ [PasswordReset] Error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update password: {str(e)}"
        )