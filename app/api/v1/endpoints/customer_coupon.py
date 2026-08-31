from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.services.customer_coupon_service import (
    CustomerCouponService,
)


router = APIRouter()


# =========================================================
# GET CUSTOMER COUPONS
# =========================================================

@router.get(
    "/coupons",
)
async def get_customer_coupons(
    current_customer=Depends(
        get_current_customer
    ),
):

    user = current_customer["user"]

    user_id = str(user.id)

    phone_number = None

    result = (
        CustomerCouponService
        .get_available_coupons(
            user_id=user_id,
            phone_number=phone_number,
        )
    )

    return result


# =========================================================
# VALIDATE COUPON
# =========================================================

@router.get(
    "/coupons/validate",
)
async def validate_customer_coupon(
    coupon_code: str,
    subtotal: float,
    service_id: str | None = None,
    phone_number: str | None = None,
    current_customer=Depends(
        get_current_customer
    ),
):

    user = current_customer["user"]

    user_id = str(user.id)

    return (
        CustomerCouponService
        .validate_coupon(
            coupon_code=coupon_code,
            user_id=user_id,
            phone_number=phone_number,
            service_id=service_id,
            subtotal=subtotal,
        )
    )


# =========================================================
# MARK COUPON USED
# =========================================================

@router.post(
    "/coupons/{coupon_id}/use",
)
async def use_customer_coupon(
    coupon_id: str,
    current_customer=Depends(
        get_current_customer
    ),
):

    user = current_customer["user"]

    user_id = str(user.id)

    return (
        CustomerCouponService
        .mark_coupon_used(
            coupon_id=coupon_id,
            user_id=user_id,
        )
    )