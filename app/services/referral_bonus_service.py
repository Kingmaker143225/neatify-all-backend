import httpx
from fastapi import HTTPException

from app.config.settings import settings


MSG91_URL = (
    "https://api.msg91.com/api/v5/whatsapp/"
    "whatsapp-outbound-message/bulk/"
)

MSG91_INTEGRATED_NUMBER = "919247542051"

MSG91_TEMPLATE_NAME = "referral_bonus_update"

MSG91_NAMESPACE = (
    "27f9a848_7c0a_47dc_bd3b_5bbd6c3a368c"
)


class ReferralBonusService:

    @staticmethod
    async def send_referral_bonus(
        referrer_phone: str,
        referrer_name: str,
        referred_friend_name: str,
        bonus_amount: str,
    ):

        # =====================================================
        # VALIDATION
        # =====================================================

        if not referrer_phone:
            raise HTTPException(
                status_code=400,
                detail="Referrer phone number is required.",
            )

        if not referrer_name:
            raise HTTPException(
                status_code=400,
                detail="Referrer name is required.",
            )

        if not referred_friend_name:
            raise HTTPException(
                status_code=400,
                detail="Referred friend name is required.",
            )

        if bonus_amount is None or bonus_amount == "":
            raise HTTPException(
                status_code=400,
                detail="Bonus amount is required.",
            )

        # =====================================================
        # FORMAT PHONE NUMBER
        # =====================================================
        #
        # Original Edge Function:
        #
        # remove everything except digits
        # if 10 digits → prepend 91
        #
        # =====================================================

        formatted_phone = "".join(
            character
            for character in str(referrer_phone)
            if character.isdigit()
        )

        if len(formatted_phone) == 10:
            formatted_phone = "91" + formatted_phone

        if not formatted_phone:
            raise HTTPException(
                status_code=400,
                detail="Invalid referrer phone number.",
            )

        print(
            "📲 Referral Bonus Notification:",
            {
                "referrer_phone": formatted_phone,
                "referrer_name": referrer_name,
                "referred_friend_name": referred_friend_name,
                "bonus_amount": bonus_amount,
            },
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
        # MSG91 PAYLOAD
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
                                formatted_phone
                            ],
                            "components": {
                                "body_referrer_name": {
                                    "type": "text",
                                    "value": str(referrer_name),
                                    "parameter_name": "referrer_name",
                                },
                                "body_referred_friend_name": {
                                    "type": "text",
                                    "value": str(
                                        referred_friend_name
                                    ),
                                    "parameter_name": "referred_friend_name",
                                },
                                "body_bonus_amount": {
                                    "type": "text",
                                    "value": str(bonus_amount),
                                    "parameter_name": "bonus_amount",
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
            # READ RESPONSE
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
                        "message": (
                            "MSG91 referral bonus "
                            "WhatsApp API failed."
                        ),
                        "status_code": response.status_code,
                        "response": response_data,
                    },
                )

            # =================================================
            # SUCCESS
            # =================================================

            return {
                "success": True,
                "message": "Referral Bonus WhatsApp sent!",
                "phone": formatted_phone,
                "response": response_data,
            }

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