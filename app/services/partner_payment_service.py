import httpx
from fastapi import HTTPException

from app.config.settings import settings


MSG91_URL = (
    "https://api.msg91.com/api/v5/whatsapp/"
    "whatsapp-outbound-message/bulk/"
)

MSG91_INTEGRATED_NUMBER = "919247542051"

MSG91_TEMPLATE_NAME = "partner_payement"

MSG91_NAMESPACE = (
    "27f9a848_7c0a_47dc_bd3b_5bbd6c3a368c"
)


class PartnerPaymentService:

    @staticmethod
    async def send_payment_notification(
        staff_name: str,
        amount,
        phone: str,
        date,
    ):
        # =====================================================
        # VALIDATION
        # =====================================================

        if not staff_name:
            raise HTTPException(
                status_code=400,
                detail="Staff name is required.",
            )

        if amount is None:
            raise HTTPException(
                status_code=400,
                detail="Amount is required.",
            )

        if not phone:
            raise HTTPException(
                status_code=400,
                detail="Phone number is required.",
            )

        if date is None:
            raise HTTPException(
                status_code=400,
                detail="Date is required.",
            )

        # =====================================================
        # CLEAN PHONE NUMBER
        # =====================================================

        clean_phone = phone.replace("+", "").strip()

        if not clean_phone:
            raise HTTPException(
                status_code=400,
                detail="Invalid phone number.",
            )

        # =====================================================
        # CHECK MSG91 AUTH KEY
        # =====================================================

        if not settings.msg91_auth_key:
            raise HTTPException(
                status_code=500,
                detail="MSG91 authentication key is not configured.",
            )

        # =====================================================
        # LOG
        # =====================================================

        print(
            "📲 Partner Payment Notification triggered:",
            {
                "staff_name": staff_name,
                "amount": amount,
                "phone": clean_phone,
                "date": date,
            },
        )

        # =====================================================
        # MSG91 WHATSAPP PAYLOAD
        # =====================================================

        payload = {
            "integrated_number": MSG91_INTEGRATED_NUMBER,
            "content_type": "template",
            "payload": {
                "messaging_product": "whatsapp",
                "type": "template",
                "template": {
                    "name": MSG91_TEMPLATE_NAME,
                    "language": {
                        "code": "en",
                        "policy": "deterministic",
                    },
                    "namespace": MSG91_NAMESPACE,
                    "to_and_components": [
                        {
                            "to": [
                                clean_phone
                            ],
                            "components": {
                                "body_date": {
                                    "type": "text",
                                    "value": str(date),
                                    "parameter_name": "date",
                                },
                                "body_amount": {
                                    "type": "text",
                                    "value": str(amount),
                                    "parameter_name": "amount",
                                },
                                "body_staff_name": {
                                    "type": "text",
                                    "value": str(staff_name),
                                    "parameter_name": "staff_name",
                                },
                            },
                        }
                    ],
                },
            },
        }

        # =====================================================
        # SEND TO MSG91
        # =====================================================

        try:

            async with httpx.AsyncClient(
                timeout=20
            ) as client:

                response = await client.post(
                    MSG91_URL,
                    headers={
                        "authkey": settings.msg91_auth_key,
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

            # =================================================
            # READ MSG91 RESPONSE
            # =================================================

            try:
                response_data = response.json()

            except Exception:

                response_data = {
                    "raw_response": response.text,
                }

            print(
                "📲 MSG91 HTTP Status:",
                response.status_code,
            )

            print(
                "📲 MSG91 Response:",
                response_data,
            )

            # =================================================
            # MSG91 ERROR
            # =================================================

            if response.status_code >= 400:

                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": "MSG91 WhatsApp API failed.",
                        "status_code": response.status_code,
                        "response": response_data,
                    },
                )

            # =================================================
            # SUCCESS
            # =================================================

            return {
                "success": True,
                "message": "Payment notification sent!",
                "phone": clean_phone,
                "response": response_data,
            }

        # =====================================================
        # CONNECTION ERROR
        # =====================================================

        except httpx.RequestError as error:

            print(
                "❌ MSG91 connection error:",
                str(error),
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "Unable to connect to MSG91 WhatsApp API: "
                    f"{str(error)}"
                ),
            )