from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_auth import (
    CustomerLoginRequest,
    CustomerLoginResponse,
    CustomerMeResponse,
    CustomerLogoutResponse,
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
# CUSTOMER ME
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