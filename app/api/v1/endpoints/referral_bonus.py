from fastapi import APIRouter

from app.schemas.referral_bonus import (
    ReferralBonusRequest,
)

from app.services.referral_bonus_service import (
    ReferralBonusService,
)


router = APIRouter()


# =========================================================
# SEND REFERRAL BONUS WHATSAPP
# =========================================================

@router.post("/send-referral-bonus")
async def send_referral_bonus(
    request: ReferralBonusRequest,
):

    return await ReferralBonusService.send_referral_bonus(
        referrer_phone=request.referrer_phone,
        referrer_name=request.referrer_name,
        referred_friend_name=request.referred_friend_name,
        bonus_amount=request.bonus_amount,
    )