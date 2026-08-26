# from fastapi import APIRouter, Depends

# from app.dependencies.auth import (
#     get_current_user,
# )

# from app.services.partner_duty_service import (
#     PartnerDutyService,
# )


# router = APIRouter()


# @router.post(
#     "/duty/off",
# )
# async def turn_off_duty(
#     current_user=Depends(
#         get_current_user
#     ),
# ):

#     return (
#         PartnerDutyService
#         .turn_off_duty(
#             user_id=str(
#                 current_user.id
#             )
#         )
#     )









from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies.partner import (
    get_current_partner,
)

from app.services.partner_duty_service import (
    PartnerDutyService,
)


router = APIRouter()


# =========================================================
# REQUEST MODEL
# =========================================================

class DutyOnRequest(BaseModel):
    work_start_location: Any | None = None


# =========================================================
# DUTY ON
# =========================================================

@router.post(
    "/duty/on",
)
async def turn_on_duty(
    request: DutyOnRequest,
    current_partner=Depends(
        get_current_partner
    ),
):

    return (
        PartnerDutyService
        .turn_on_duty(
            user_id=str(
                current_partner["id"]
            ),
            work_start_location=(
                request.work_start_location
            ),
        )
    )


# =========================================================
# DUTY OFF
# =========================================================

@router.post(
    "/duty/off",
)
async def turn_off_duty(
    current_partner=Depends(
        get_current_partner
    ),
):

    return (
        PartnerDutyService
        .turn_off_duty(
            user_id=str(
                current_partner["id"]
            )
        )
    )