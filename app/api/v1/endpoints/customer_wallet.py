from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.services.customer_wallet_service import (
    CustomerWalletService,
)


router = APIRouter()


# =========================================================
# GET CUSTOMER WALLET
# =========================================================

@router.get(
    "/wallet",
)
async def get_customer_wallet(
    current_customer=Depends(
        get_current_customer
    ),
):

    user = current_customer["user"]

    user_id = str(user.id)

    return (
        CustomerWalletService
        .get_wallet(
            user_id=user_id,
        )
    )


# =========================================================
# GET WALLET TRANSACTIONS
# =========================================================

@router.get(
    "/wallet/transactions",
)
async def get_customer_wallet_transactions(
    limit: int = 50,
    current_customer=Depends(
        get_current_customer
    ),
):

    user = current_customer["user"]

    user_id = str(user.id)

    return (
        CustomerWalletService
        .get_transactions(
            user_id=user_id,
            limit=limit,
        )
    )


# =========================================================
# DEDUCT WALLET
# =========================================================

@router.post(
    "/wallet/deduct",
)
async def deduct_customer_wallet(
    amount: float,
    description: str = "Booking payment",
    current_customer=Depends(
        get_current_customer
    ),
):

    user = current_customer["user"]

    user_id = str(user.id)

    return (
        CustomerWalletService
        .deduct_wallet(
            user_id=user_id,
            amount=amount,
            description=description,
        )
    )