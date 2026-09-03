# from fastapi import APIRouter

# from app.schemas.notification import (
#     SendStaffNotificationRequest,
#     StaffNotificationRequest,
# )

# from app.services.partner_notification_service import (
#     PartnerNotificationService,
# )


# router = APIRouter()


# # =========================================================
# # SEND STAFF NOTIFICATION DIRECTLY TO PUSH TOKEN
# # =========================================================

# @router.post("/send-staff-notification")
# async def send_staff_notification(
#     request: SendStaffNotificationRequest,
# ):
#     return await PartnerNotificationService.send_to_token(
#         token=request.token,
#         title=request.title,
#         body=request.body,
#         data=request.data,
#     )


# # =========================================================
# # FIND STAFF BY EMAIL AND SEND NOTIFICATION
# # =========================================================

# @router.post("/staff-notification")
# async def staff_notification(
#     request: StaffNotificationRequest,
# ):
#     return await PartnerNotificationService.send_staff_notification(
#         email=request.email,
#         title=request.title,
#         body=request.body,
#         data=request.data,
#     )















from fastapi import APIRouter

from app.schemas.notification import (
    SendStaffNotificationRequest,
    StaffNotificationRequest,
)

from app.services.partner_notification_service import (
    PartnerNotificationService,
)

from app.services.staff_notification_service import (
    StaffNotificationService,
)


router = APIRouter()


# =========================================================
# SEND STAFF NOTIFICATION DIRECTLY TO PUSH TOKEN
# =========================================================

@router.post("/send-staff-notification")
async def send_staff_notification(
    request: SendStaffNotificationRequest,
):
    return await PartnerNotificationService.send_to_token(
        token=request.token,
        title=request.title,
        body=request.body,
        data=request.data,
    )


# =========================================================
# FIND STAFF BY EMAIL AND SEND NOTIFICATION
# =========================================================

@router.post("/staff-notification")
async def staff_notification(
    request: StaffNotificationRequest,
):
    return await StaffNotificationService.send_staff_notification(
        email=request.email,
        title=request.title,
        body=request.body,
    )