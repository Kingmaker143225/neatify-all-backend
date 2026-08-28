from pydantic import BaseModel, Field


class CustomerPaymentCreateOrderRequest(BaseModel):
    booking_id: str


class CustomerPaymentCreateOrderResponse(BaseModel):
    success: bool
    booking_id: str
    razorpay_order_id: str
    amount: int
    currency: str
    razorpay_key_id: str


class CustomerPaymentVerifyRequest(BaseModel):
    booking_id: str

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class CustomerPaymentVerifyResponse(BaseModel):
    success: bool
    booking_id: str
    payment_status: str
    payment_verified: bool
    message: str