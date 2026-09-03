from fastapi import APIRouter

from app.schemas.staff_notification import (
    StaffNotificationRequest,
)

from app.services.staff_notification_service import (
    StaffNotificationService,
)


router = APIRouter()


# =========================================================
# STAFF NOTIFICATION
# =========================================================

@router.post("/staff-notification")
async def staff_notification(
    request: StaffNotificationRequest,
):

    return (
        await StaffNotificationService
        .send_staff_notification(
            email=request.email,
            title=request.title,
            body=request.body,
        )
    )