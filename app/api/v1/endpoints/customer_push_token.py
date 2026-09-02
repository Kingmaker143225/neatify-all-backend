from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_push_token import (
    CustomerPushTokenRequest,
)

from app.services.customer_push_token_service import (
    CustomerPushTokenService,
)


router = APIRouter()


# =========================================================
# SAVE CUSTOMER PUSH TOKEN
# =========================================================

@router.post(
    "/push-token",
)
async def save_customer_push_token(
    request: CustomerPushTokenRequest,
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerPushTokenService
        .save_token(
            user_id=user_id,
            token=request.token,
            platform=request.platform,
        )
    )


# =========================================================
# REMOVE CUSTOMER PUSH TOKEN
# =========================================================

@router.delete(
    "/push-token",
)
async def remove_customer_push_token(
    request: CustomerPushTokenRequest,
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerPushTokenService
        .remove_token(
            user_id=user_id,
            token=request.token,
        )
    )