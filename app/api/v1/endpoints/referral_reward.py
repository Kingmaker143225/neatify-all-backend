from fastapi import APIRouter

from app.schemas.referral_reward import (
    ReferralRewardRequest,
)

from app.services.referral_reward_service import (
    ReferralRewardService,
)


router = APIRouter()


# =========================================================
# SEND REFERRAL REWARD WHATSAPP
# =========================================================

@router.post("/send-referral-reward")
async def send_referral_reward(
    request: ReferralRewardRequest,
):

    return await ReferralRewardService.send_referral_reward(
        staff_name=request.staff_name,
        referred_person_name=request.referred_person_name,
        amount=request.amount,
        phone=request.phone,
    )