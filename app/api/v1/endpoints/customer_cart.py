from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_cart import (
    CustomerCartItemAddRequest,
    CustomerCartItemResponse,
    CustomerCartResponse,
)

from app.services.customer_cart_service import (
    CustomerCartService,
)


router = APIRouter()


# =========================================================
# GET CUSTOMER CART
# =========================================================

@router.get(
    "",
    response_model=CustomerCartResponse,
)
async def get_customer_cart(
    current_customer=Depends(
        get_current_customer
    ),
):
    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerCartService
        .get_cart(
            user_id=user_id,
        )
    )


# =========================================================
# ADD SERVICE TO CART
# =========================================================

@router.post(
    "",
)
async def add_customer_cart_item(
    request: CustomerCartItemAddRequest,
    current_customer=Depends(
        get_current_customer
    ),
):
    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerCartService
        .add_to_cart(
            user_id=user_id,
            service_id=request.service_id,
        )
    )


# =========================================================
# REMOVE SERVICE FROM CART
# =========================================================

@router.delete(
    "/{service_id}",
)
async def remove_customer_cart_item(
    service_id: str,
    current_customer=Depends(
        get_current_customer
    ),
):
    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerCartService
        .remove_from_cart(
            user_id=user_id,
            service_id=service_id,
        )
    )


# =========================================================
# CLEAR CUSTOMER CART
# =========================================================

@router.delete(
    "",
)
async def clear_customer_cart(
    current_customer=Depends(
        get_current_customer
    ),
):
    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerCartService
        .clear_cart(
            user_id=user_id,
        )
    )