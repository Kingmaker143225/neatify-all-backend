from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_payment import (
    CustomerPaymentCreateOrderRequest,
    CustomerPaymentCreateOrderResponse,
    CustomerPaymentVerifyRequest,
    CustomerPaymentVerifyResponse,
)

from app.services.customer_payment_service import (
    CustomerPaymentService,
)


router = APIRouter()


# =========================================================
# CREATE RAZORPAY ORDER
# =========================================================

@router.post(
    "/payment/create-order",
    response_model=CustomerPaymentCreateOrderResponse,
)
async def create_customer_payment_order(
    request: CustomerPaymentCreateOrderRequest,
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = current_customer["user"].id

    return (
        CustomerPaymentService
        .create_order(
            booking_id=request.booking_id,
            user_id=str(user_id),
        )
    )


# =========================================================
# VERIFY RAZORPAY PAYMENT
# =========================================================

@router.post(
    "/payment/verify",
    response_model=CustomerPaymentVerifyResponse,
)
async def verify_customer_payment(
    request: CustomerPaymentVerifyRequest,
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = current_customer["user"].id

    return (
        CustomerPaymentService
        .verify_payment(
            booking_id=request.booking_id,
            user_id=str(user_id),
            razorpay_order_id=(
                request.razorpay_order_id
            ),
            razorpay_payment_id=(
                request.razorpay_payment_id
            ),
            razorpay_signature=(
                request.razorpay_signature
            ),
        )
    )