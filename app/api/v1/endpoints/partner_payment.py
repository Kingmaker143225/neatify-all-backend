from fastapi import APIRouter

from app.schemas.partner_payment import (
    PartnerPaymentRequest,
)

from app.services.partner_payment_service import (
    PartnerPaymentService,
)


router = APIRouter()


# =========================================================
# SEND PARTNER PAYMENT WHATSAPP
# =========================================================

@router.post("/send-partner-payment")
async def send_partner_payment(
    request: PartnerPaymentRequest,
):

    return await PartnerPaymentService.send_payment_notification(
        staff_name=request.staff_name,
        amount=request.amount,
        phone=request.phone,
        date=request.date,
    )