from fastapi import APIRouter

from app.services.referral_milestone_service import (
    ReferralMilestoneService,
)


router = APIRouter()


# =========================================================
# CHECK REFERRAL MILESTONES
# =========================================================

@router.post("/check-referral-milestones")
async def check_referral_milestones():

    return await ReferralMilestoneService.check_milestones()