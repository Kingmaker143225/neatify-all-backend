# from fastapi import (
#     APIRouter,
#     Depends,
#     File,
#     Form,
#     HTTPException,
#     UploadFile,
# )

# from pydantic import BaseModel

# from app.dependencies.partner import get_current_partner

# from app.schemas.partner_dashboard import (
#     PartnerDashboardResponse,
# )

# from app.services.partner_dashboard_service import (
#     PartnerDashboardService,
# )

# from app.services.partner_booking_service import (
#     PartnerBookingService,
# )

# from app.schemas.partner_booking_action import (
#     RejectBookingRequest,
#     BookingActionResponse,
# )

# from app.services.partner_booking_action_service import (
#     PartnerBookingActionService,
# )

# from app.repositories.partner_booking_repository import (
#     PartnerBookingRepository,
# )


# router = APIRouter()


# # =========================================================
# # REQUEST MODEL - CANCEL BOOKING
# # =========================================================

# class CancelBookingRequest(BaseModel):
#     reason: str


# # =========================================================
# # PROFILE
# # =========================================================

# @router.get("/profile")
# async def get_profile(
#     partner=Depends(get_current_partner),
# ):
#     return {
#         "success": True,
#         "data": partner,
#     }


# # =========================================================
# # DASHBOARD
# # =========================================================

# @router.get(
#     "/dashboard",
#     response_model=PartnerDashboardResponse,
# )
# async def get_partner_dashboard(
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerDashboardService.get_dashboard(
#         str(current_partner["id"])
#     )


# # =========================================================
# # GET PARTNER BOOKINGS
# # =========================================================

# @router.get("/bookings")
# async def get_partner_bookings(
#     current_partner=Depends(get_current_partner),
#     status: str | None = None,
# ):
#     email = current_partner.get("email")

#     bookings = PartnerBookingService.get_bookings(
#         email=email,
#         status=status,
#     )

#     return {
#         "success": True,
#         "count": len(bookings),
#         "data": bookings,
#     }


# # =========================================================
# # APPROVE BOOKING
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/approve",
#     response_model=BookingActionResponse,
# )
# async def approve_booking(
#     booking_id: str,
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerBookingActionService.approve(
#         booking_id=booking_id,
#         email=current_partner["email"],
#     )


# # =========================================================
# # REJECT BOOKING
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/reject",
#     response_model=BookingActionResponse,
# )
# async def reject_booking(
#     booking_id: str,
#     request: RejectBookingRequest,
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerBookingActionService.reject(
#         booking_id=booking_id,
#         email=current_partner["email"],
#         reason=request.reason,
#     )


# # =========================================================
# # CANCEL ASSIGNED BOOKING
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/cancel",
# )
# async def cancel_booking(
#     booking_id: str,
#     request: CancelBookingRequest,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingActionService
#         .cancel(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             reason=request.reason,
#         )
#     )


# # =========================================================
# # BOOKING DETAILS
# # =========================================================

# @router.get(
#     "/bookings/{booking_id}/details"
# )
# async def get_booking_details(
#     booking_id: str,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .get_booking_details(
#             booking_id=booking_id,
#             email=current_partner["email"],
#         )
#     )


# # =========================================================
# # START WORK
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/start"
# )
# async def start_work(
#     booking_id: str,
#     start_otp: str = Form(...),
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .start_work(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             start_otp=start_otp,
#         )
#     )


# # =========================================================
# # COMPLETE WORK
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/complete"
# )
# async def complete_work(
#     booking_id: str,
#     end_otp: str = Form(...),
#     worked_duration: str = Form(...),
#     staff_amount: float = Form(...),
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .complete_work(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             end_otp=end_otp,
#             worked_duration=worked_duration,
#             staff_amount=staff_amount,
#         )
#     )


# # =========================================================
# # SKIP PHOTO
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/skip-photo"
# )
# async def skip_photo(
#     booking_id: str,
#     stage: str = Form(...),
#     reason: str = Form(...),
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .skip_photo(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             stage=stage,
#             reason=reason,
#         )
#     )


# # =========================================================
# # PHOTO UPLOAD
# # =========================================================

# @router.post(
#     "/bookings/{booking_id}/photos"
# )
# async def upload_photo(
#     booking_id: str,
#     stage: str = Form(...),
#     category: str = Form(...),
#     file: UploadFile = File(...),
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):

#     # ---------------------------------------------------------
#     # Validate photo stage
#     # ---------------------------------------------------------

#     if stage not in (
#         "before",
#         "after",
#     ):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid photo stage.",
#         )

#     # ---------------------------------------------------------
#     # Verify booking belongs to partner
#     # ---------------------------------------------------------

#     booking = (
#         PartnerBookingRepository
#         .get_booking_for_partner(
#             booking_id=booking_id,
#             email=current_partner["email"],
#         )
#     )

#     if not booking:
#         raise HTTPException(
#             status_code=404,
#             detail="Booking not found.",
#         )

#     # ---------------------------------------------------------
#     # Read uploaded file
#     # ---------------------------------------------------------

#     file_bytes = await file.read()

#     if not file_bytes:
#         raise HTTPException(
#             status_code=400,
#             detail="Uploaded file is empty.",
#         )

#     # ---------------------------------------------------------
#     # Save photo
#     # ---------------------------------------------------------

#     result = (
#         PartnerBookingRepository
#         .save_photo(
#             booking=booking,
#             email=current_partner["email"],
#             stage=stage,
#             category=category,
#             file_bytes=file_bytes,
#             content_type=(
#                 file.content_type
#                 or "image/jpeg"
#             ),
#         )
#     )

#     return {
#         "success": True,
#         "message": "Photo uploaded successfully.",
#         "data": result,
#     }































# from fastapi import (
#     APIRouter,
#     Depends,
#     File,
#     Form,
#     HTTPException,
#     UploadFile,
# )

# from pydantic import BaseModel

# from app.dependencies.partner import get_current_partner

# from app.schemas.partner_dashboard import (
#     PartnerDashboardResponse,
# )

# from app.services.partner_dashboard_service import (
#     PartnerDashboardService,
# )

# from app.services.partner_booking_service import (
#     PartnerBookingService,
# )

# from app.schemas.partner_booking_action import (
#     RejectBookingRequest,
#     BookingActionResponse,
# )

# from app.services.partner_booking_action_service import (
#     PartnerBookingActionService,
# )

# from app.repositories.partner_booking_repository import (
#     PartnerBookingRepository,
# )


# from app.services.partner_zone_service import (
#     PartnerZoneService,
# )

# from fastapi import Depends, Query

# from app.dependencies.partner import get_current_partner
# from app.services.partner_earnings_service import (
#     PartnerEarningsService,
# )

# from app.services.partner_referral_service import (
#     PartnerReferralService,
# )

# from app.services.partner_notification_service import (
#     PartnerNotificationService,
# )

# from app.services.partner_hero_service import (
#     PartnerHeroService,
# )

# router = APIRouter()


# # =========================================================
# # REQUEST MODELS
# # =========================================================


# class CancelBookingRequest(BaseModel):
#     reason: str


# class StartWorkRequest(BaseModel):
#     start_otp: str


# class CompleteWorkRequest(BaseModel):
#     end_otp: str
#     worked_duration: str
#     staff_amount: float


# class SkipPhotoRequest(BaseModel):
#     stage: str
#     reason: str


# class PartnerLocationRequest(BaseModel):
#     latitude: float | None = None
#     longitude: float | None = None
#     is_out_of_zone: bool | None = None

# # =========================================================
# # PROFILE
# # =========================================================


# @router.get("/profile")
# async def get_profile(
#     partner=Depends(get_current_partner),
# ):
#     return {
#         "success": True,
#         "data": partner,
#     }


# # =========================================================
# # DASHBOARD
# # =========================================================


# @router.get(
#     "/dashboard",
#     response_model=PartnerDashboardResponse,
# )
# async def get_partner_dashboard(
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerDashboardService.get_dashboard(
#         str(current_partner["id"])
#     )

# # =========================================================
# # PARTNER ZONE
# # =========================================================


# @router.get("/zone")
# async def get_partner_zone(
#     current_partner=Depends(get_current_partner),
# ):
#     """
#     Get the authenticated partner's assigned work zone.
#     """

#     return {
#         "success": True,
#         "data": PartnerZoneService.get_zone(
#             email=current_partner["email"]
#         ),
#     }


# # =========================================================
# # UPDATE PARTNER LOCATION / ZONE STATUS
# # =========================================================


# @router.patch("/location")
# async def update_partner_location(
#     request: PartnerLocationRequest,
#     current_partner=Depends(get_current_partner),
# ):
#     """
#     Update the authenticated partner's live location
#     and out-of-zone status.
#     """

#     live_location = None

#     if (
#         request.latitude is not None
#         and request.longitude is not None
#     ):
#         live_location = (
#             f"{request.latitude},{request.longitude}"
#         )

#     return PartnerZoneService.update_location(
#         email=current_partner["email"],
#         live_location=live_location,
#         is_out_of_zone=request.is_out_of_zone,
#     )
# # =========================================================
# # WEEKLY EARNINGS
# # =========================================================

# @router.get("/earnings/weekly")
# async def get_weekly_earnings(
#     year: int = Query(...),
#     month: int = Query(..., ge=1, le=12),
#     week: int = Query(..., ge=1, le=6),
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerEarningsService.get_weekly_earnings(
#         staff_email=staff_email,
#         year=year,
#         month=month,
#         week=week,
#     )

# # =========================================================
# # MONTHLY EARNINGS
# # =========================================================

# @router.get("/earnings/monthly")
# async def get_monthly_earnings(
#     year: int = Query(...),
#     month: int = Query(..., ge=1, le=12),
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerEarningsService.get_monthly_earnings(
#         staff_email=staff_email,
#         year=year,
#         month=month,
#     )

# # =========================================================
# # PENDING PAYMENTS
# # =========================================================

# @router.get("/earnings/pending")
# async def get_pending_payments(
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerEarningsService.get_pending_payments(
#         staff_email=staff_email,
#     )
# # =========================================================
# # TOTAL EARNINGS
# # =========================================================

# @router.get("/earnings/total")
# async def get_total_earnings(
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerEarningsService.get_total_earnings(
#         staff_email=staff_email,
#     )

# # =========================================================
# # REFERRAL SUMMARY
# # =========================================================

# @router.get("/referrals")
# async def get_referral_summary(
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerReferralService
#         .get_referral_summary(
#             partner_id=current_partner["id"]
#         )
#     )


# # =========================================================
# # REFERRAL HISTORY
# # =========================================================

# @router.get("/referrals/history")
# async def get_referral_history(
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerReferralService
#         .get_referral_history(
#             partner_id=current_partner["id"]
#         )
#     )
# # =========================================================
# # GET PARTNER BOOKINGS
# # =========================================================


# @router.get("/bookings")
# async def get_partner_bookings(
#     current_partner=Depends(get_current_partner),
#     status: str | None = None,
# ):
#     email = current_partner.get("email")

#     bookings = PartnerBookingService.get_bookings(
#         email=email,
#         status=status,
#     )

#     return {
#         "success": True,
#         "count": len(bookings),
#         "data": bookings,
#     }


# # =========================================================
# # APPROVE BOOKING
# # =========================================================


# @router.post(
#     "/bookings/{booking_id}/approve",
#     response_model=BookingActionResponse,
# )
# async def approve_booking(
#     booking_id: str,
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerBookingActionService.approve(
#         booking_id=booking_id,
#         email=current_partner["email"],
#     )


# # =========================================================
# # REJECT BOOKING
# # =========================================================


# @router.post(
#     "/bookings/{booking_id}/reject",
#     response_model=BookingActionResponse,
# )
# async def reject_booking(
#     booking_id: str,
#     request: RejectBookingRequest,
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerBookingActionService.reject(
#         booking_id=booking_id,
#         email=current_partner["email"],
#         reason=request.reason,
#     )


# # =========================================================
# # CANCEL ASSIGNED BOOKING
# # =========================================================


# @router.post(
#     "/bookings/{booking_id}/cancel",
# )
# async def cancel_booking(
#     booking_id: str,
#     request: CancelBookingRequest,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingActionService
#         .cancel(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             reason=request.reason,
#         )
#     )


# # =========================================================
# # BOOKING DETAILS
# # =========================================================


# @router.get(
#     "/bookings/{booking_id}/details"
# )
# async def get_booking_details(
#     booking_id: str,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .get_booking_details(
#             booking_id=booking_id,
#             email=current_partner["email"],
#         )
#     )


# # =========================================================
# # START WORK
# # =========================================================


# @router.post(
#     "/bookings/{booking_id}/start"
# )
# async def start_work(
#     booking_id: str,
#     request: StartWorkRequest,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .start_work(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             start_otp=request.start_otp,
#         )
#     )


# # =========================================================
# # COMPLETE WORK
# # =========================================================


# @router.post(
#     "/bookings/{booking_id}/complete"
# )
# async def complete_work(
#     booking_id: str,
#     request: CompleteWorkRequest,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .complete_work(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             end_otp=request.end_otp,
#             worked_duration=request.worked_duration,
#             staff_amount=request.staff_amount,
#         )
#     )


# # =========================================================
# # SKIP PHOTO
# # =========================================================


# # @router.post(
# #     "/bookings/{booking_id}/skip-photo"
# # )
# # async def skip_photo(
# #     booking_id: str,
# #     request: SkipPhotoRequest,
# #     current_partner=Depends(
# #         get_current_partner
# #     ),
# # ):
# #     return (
# #         PartnerBookingService
# #         .skip_photo(
# #             booking_id=booking_id,
# #             email=current_partner["email"],
# #             stage=request.stage,
# #             reason=request.reason,
# #         )
# #     )


# # =========================================================
# # SKIP PHOTO
# # =========================================================

# class SkipPhotoRequest(BaseModel):
#     stage: str
#     reason: str


# @router.post(
#     "/bookings/{booking_id}/skip-photo"
# )
# async def skip_photo(
#     booking_id: str,
#     request: SkipPhotoRequest,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):

#     return (
#         PartnerBookingService
#         .skip_photo(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             stage=request.stage,
#             reason=request.reason,
#         )
#     )

# # =========================================================
# # PHOTO UPLOAD
# # =========================================================


# @router.post(
#     "/bookings/{booking_id}/photos"
# )
# async def upload_photo(
#     booking_id: str,
#     stage: str = Form(...),
#     category: str = Form(...),
#     file: UploadFile = File(...),
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):

#     # ---------------------------------------------------------
#     # VALIDATE PHOTO STAGE
#     # ---------------------------------------------------------

#     if stage not in (
#         "before",
#         "after",
#     ):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid photo stage.",
#         )

#     # ---------------------------------------------------------
#     # VERIFY BOOKING BELONGS TO PARTNER
#     # ---------------------------------------------------------

#     booking = (
#         PartnerBookingRepository
#         .get_booking_for_partner(
#             booking_id=booking_id,
#             email=current_partner["email"],
#         )
#     )

#     if not booking:
#         raise HTTPException(
#             status_code=404,
#             detail="Booking not found.",
#         )

#     # ---------------------------------------------------------
#     # VERIFY BOOKING IS ACTIVE
#     # ---------------------------------------------------------

#     work_status = str(
#         booking.get("work_status") or ""
#     ).strip().upper()

#     if work_status in (
#         "COMPLETED",
#         "CANCELLED",
#     ):
#         raise HTTPException(
#             status_code=409,
#             detail="This booking is no longer active.",
#         )

#     # ---------------------------------------------------------
#     # READ FILE
#     # ---------------------------------------------------------

#     file_bytes = await file.read()

#     if not file_bytes:
#         raise HTTPException(
#             status_code=400,
#             detail="Uploaded file is empty.",
#         )

#     # ---------------------------------------------------------
#     # SAVE PHOTO THROUGH REPOSITORY
#     # ---------------------------------------------------------

#     try:

#         result = (
#             PartnerBookingRepository
#             .save_photo(
#                 booking=booking,
#                 email=current_partner["email"],
#                 stage=stage,
#                 category=category,
#                 file_bytes=file_bytes,
#                 content_type=(
#                     file.content_type
#                     or "image/jpeg"
#                 ),
#             )
#         )

#     except ValueError as error:

#         raise HTTPException(
#             status_code=400,
#             detail=str(error),
#         )

#     except Exception as error:

#         print(
#             "PHOTO UPLOAD ERROR:",
#             repr(error),
#         )

#         raise HTTPException(
#             status_code=500,
#             detail=(
#                 f"Photo upload failed: {str(error)}"
#             ),
#         )

#     # ---------------------------------------------------------
#     # RESPONSE
#     # ---------------------------------------------------------

#     return {
#         "success": True,
#         "message": "Photo uploaded successfully.",
#         "data": result,
#     }

# # =========================================================
# # NOTIFICATIONS
# # =========================================================

# @router.get("/notifications")
# async def get_notifications(
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerNotificationService.get_notifications(
#         staff_email=staff_email,
#     )


# @router.patch("/notifications/{notification_id}/read")
# async def mark_notification_read(
#     notification_id: str,
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerNotificationService.mark_as_read(
#         notification_id=notification_id,
#         staff_email=staff_email,
#     )


# @router.delete("/notifications/{notification_id}")
# async def delete_notification(
#     notification_id: str,
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerNotificationService.delete_notification(
#         notification_id=notification_id,
#         staff_email=staff_email,
#     )


# @router.delete("/notifications")
# async def delete_all_notifications(
#     current_partner=Depends(get_current_partner),
# ):
#     staff_email = current_partner["email"]

#     return PartnerNotificationService.delete_all_notifications(
#         staff_email=staff_email,
#     )

# # =========================================================
# # HERO IMAGES
# # =========================================================

# @router.get("/hero-images")
# async def get_hero_images(
#     current_partner=Depends(get_current_partner),
# ):
#     return PartnerHeroService.get_hero_images()


















from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from pydantic import BaseModel

from app.dependencies.partner import get_current_partner

from app.schemas.partner_dashboard import (
    PartnerDashboardResponse,
)

from app.services.partner_dashboard_service import (
    PartnerDashboardService,
)

from app.services.partner_booking_service import (
    PartnerBookingService,
)

from app.schemas.partner_booking_action import (
    RejectBookingRequest,
    BookingActionResponse,
)

from app.services.partner_booking_action_service import (
    PartnerBookingActionService,
)

from app.repositories.partner_booking_repository import (
    PartnerBookingRepository,
)


from app.services.partner_zone_service import (
    PartnerZoneService,
)

from fastapi import Depends, Query

from app.dependencies.partner import get_current_partner
from app.services.partner_earnings_service import (
    PartnerEarningsService,
)

from app.services.partner_referral_service import (
    PartnerReferralService,
)

from app.services.partner_notification_service import (
    PartnerNotificationService,
)

from app.services.partner_hero_service import (
    PartnerHeroService,
)


from app.supabase.admin_client import supabase_admin

# from fastapi import Depends

# from app.schemas.availability import (
#     AvailabilitySaveRequest,
# )
# from app.services.availability_service import (
#     AvailabilityService,
# )




from fastapi import Query

from app.schemas.availability import AvailabilitySaveRequest
from app.services.availability_service import AvailabilityService
router = APIRouter()


# =========================================================
# REQUEST MODELS
# =========================================================


class CancelBookingRequest(BaseModel):
    reason: str


class StartWorkRequest(BaseModel):
    start_otp: str


class CompleteWorkRequest(BaseModel):
    end_otp: str
    worked_duration: str
    staff_amount: float


class SkipPhotoRequest(BaseModel):
    stage: str
    reason: str


class PartnerLocationRequest(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    is_out_of_zone: bool | None = None

class PartnerLocationAlertRequest(BaseModel):
    alert_type: str
    current_location: str
    assigned_hub: str

class PushTokenRequest(BaseModel):
    push_token: str


class PartnerLocationAlertRequest(BaseModel):
    alert_type: str
    current_location: str
    assigned_hub: str

class PushTokenRequest(BaseModel):
    push_token: str


class PricingDetailsResponse(BaseModel):
    service_charge_percentage: float
    gst_percentage: float
    platform_fee_percentage: float

# =========================================================
# PROFILE
# =========================================================


@router.get("/profile")
async def get_profile(
    partner=Depends(get_current_partner),
):
    return {
        "success": True,
        "data": partner,
    }


# =========================================================
# DASHBOARD
# =========================================================


@router.get(
    "/dashboard",
    response_model=PartnerDashboardResponse,
)
async def get_partner_dashboard(
    current_partner=Depends(get_current_partner),
):
    return PartnerDashboardService.get_dashboard(
        str(current_partner["id"])
    )

# =========================================================
# PARTNER ZONE
# =========================================================


@router.get("/zone")
async def get_partner_zone(
    current_partner=Depends(get_current_partner),
):
    """
    Get the authenticated partner's assigned work zone.
    """

    return {
        "success": True,
        "data": PartnerZoneService.get_zone(
            email=current_partner["email"]
        ),
    }


# =========================================================
# UPDATE PARTNER LOCATION / ZONE STATUS
# =========================================================


@router.patch("/location")
async def update_partner_location(
    request: PartnerLocationRequest,
    current_partner=Depends(get_current_partner),
):
    """
    Update the authenticated partner's live location
    and out-of-zone status.
    """

    live_location = None

    if (
        request.latitude is not None
        and request.longitude is not None
    ):
        live_location = (
            f"{request.latitude},{request.longitude}"
        )

    return PartnerZoneService.update_location(
        email=current_partner["email"],
        live_location=live_location,
        is_out_of_zone=request.is_out_of_zone,
    )
# =========================================================
# OUT OF ZONE LOCATION ALERT
# =========================================================

@router.post("/location-alerts")
async def create_location_alert(
    request: PartnerLocationAlertRequest,
    current_partner=Depends(get_current_partner),
):
    """
    Receive an out-of-zone alert from the partner app.

    This endpoint does not create a database table
    or store a separate alert record.

    It simply confirms that the authenticated partner's
    alert was received successfully.
    """

    partner_email = current_partner["email"]

    print(
        "🚨 PARTNER LOCATION ALERT:",
        {
            "partner_email": partner_email,
            "alert_type": request.alert_type,
            "current_location": request.current_location,
            "assigned_hub": request.assigned_hub,
        },
    )

    return {
        "success": True,
        "message": "Location alert received successfully.",
        "data": {
            "alert_type": request.alert_type,
            "current_location": request.current_location,
            "assigned_hub": request.assigned_hub,
        },
    }


# =========================================================
# PRICING DETAILS
# =========================================================

@router.get("/pricing-details")
async def get_pricing_details(
    current_partner=Depends(get_current_partner),
):

    response = (
        supabase_admin
        .table("services")
        .select("id,title,staff_amount")
        .order("title")
        .execute()
    )

    return {
        "success": True,
        "data": response.data,
    }
# =========================================================
# WEEKLY EARNINGS
# =========================================================

@router.get("/earnings/weekly")
async def get_weekly_earnings(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    week: int = Query(..., ge=1, le=6),
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerEarningsService.get_weekly_earnings(
        staff_email=staff_email,
        year=year,
        month=month,
        week=week,
    )

# =========================================================
# MONTHLY EARNINGS
# =========================================================

@router.get("/earnings/monthly")
async def get_monthly_earnings(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerEarningsService.get_monthly_earnings(
        staff_email=staff_email,
        year=year,
        month=month,
    )

# =========================================================
# PENDING PAYMENTS
# =========================================================

@router.get("/earnings/pending")
async def get_pending_payments(
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerEarningsService.get_pending_payments(
        staff_email=staff_email,
    )
# =========================================================
# TOTAL EARNINGS
# =========================================================

@router.get("/earnings/total")
async def get_total_earnings(
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerEarningsService.get_total_earnings(
        staff_email=staff_email,
    )

# =========================================================
# REFERRAL SUMMARY
# =========================================================

@router.get("/referrals")
async def get_referral_summary(
    current_partner=Depends(
        get_current_partner
    ),
):
    return (
        PartnerReferralService
        .get_referral_summary(
            partner_id=current_partner["id"]
        )
    )


# =========================================================
# REFERRAL HISTORY
# =========================================================

@router.get("/referrals/history")
async def get_referral_history(
    current_partner=Depends(
        get_current_partner
    ),
):
    return (
        PartnerReferralService
        .get_referral_history(
            partner_id=current_partner["id"]
        )
    )
# =========================================================
# GET PARTNER BOOKINGS
# =========================================================


@router.get("/bookings")
async def get_partner_bookings(
    current_partner=Depends(get_current_partner),
    status: str | None = None,
):
    email = current_partner.get("email")

    bookings = PartnerBookingService.get_bookings(
        email=email,
        status=status,
    )

    return {
        "success": True,
        "count": len(bookings),
        "data": bookings,
    }


# =========================================================
# APPROVE BOOKING
# =========================================================


@router.post(
    "/bookings/{booking_id}/approve",
    response_model=BookingActionResponse,
)
async def approve_booking(
    booking_id: str,
    current_partner=Depends(get_current_partner),
):
    return PartnerBookingActionService.approve(
        booking_id=booking_id,
        email=current_partner["email"],
    )


# =========================================================
# REJECT BOOKING
# =========================================================


@router.post(
    "/bookings/{booking_id}/reject",
    response_model=BookingActionResponse,
)
async def reject_booking(
    booking_id: str,
    request: RejectBookingRequest,
    current_partner=Depends(get_current_partner),
):
    return PartnerBookingActionService.reject(
        booking_id=booking_id,
        email=current_partner["email"],
        reason=request.reason,
    )


# =========================================================
# CANCEL ASSIGNED BOOKING
# =========================================================


@router.post(
    "/bookings/{booking_id}/cancel",
)
async def cancel_booking(
    booking_id: str,
    request: CancelBookingRequest,
    current_partner=Depends(
        get_current_partner
    ),
):
    return (
        PartnerBookingActionService
        .cancel(
            booking_id=booking_id,
            email=current_partner["email"],
            reason=request.reason,
        )
    )


# =========================================================
# BOOKING DETAILS
# =========================================================


@router.get(
    "/bookings/{booking_id}/details"
)
async def get_booking_details(
    booking_id: str,
    current_partner=Depends(
        get_current_partner
    ),
):
    return (
        PartnerBookingService
        .get_booking_details(
            booking_id=booking_id,
            email=current_partner["email"],
        )
    )


# =========================================================
# START WORK
# =========================================================


@router.post(
    "/bookings/{booking_id}/start"
)
async def start_work(
    booking_id: str,
    request: StartWorkRequest,
    current_partner=Depends(
        get_current_partner
    ),
):
    return (
        PartnerBookingService
        .start_work(
            booking_id=booking_id,
            email=current_partner["email"],
            start_otp=request.start_otp,
        )
    )


# =========================================================
# COMPLETE WORK
# =========================================================


@router.post(
    "/bookings/{booking_id}/complete"
)
async def complete_work(
    booking_id: str,
    request: CompleteWorkRequest,
    current_partner=Depends(
        get_current_partner
    ),
):
    return (
        PartnerBookingService
        .complete_work(
            booking_id=booking_id,
            email=current_partner["email"],
            end_otp=request.end_otp,
            worked_duration=request.worked_duration,
            staff_amount=request.staff_amount,
        )
    )


# =========================================================
# SKIP PHOTO
# =========================================================


# @router.post(
#     "/bookings/{booking_id}/skip-photo"
# )
# async def skip_photo(
#     booking_id: str,
#     request: SkipPhotoRequest,
#     current_partner=Depends(
#         get_current_partner
#     ),
# ):
#     return (
#         PartnerBookingService
#         .skip_photo(
#             booking_id=booking_id,
#             email=current_partner["email"],
#             stage=request.stage,
#             reason=request.reason,
#         )
#     )


# =========================================================
# SKIP PHOTO
# =========================================================

class SkipPhotoRequest(BaseModel):
    stage: str
    reason: str


@router.post(
    "/bookings/{booking_id}/skip-photo"
)
async def skip_photo(
    booking_id: str,
    request: SkipPhotoRequest,
    current_partner=Depends(
        get_current_partner
    ),
):

    return (
        PartnerBookingService
        .skip_photo(
            booking_id=booking_id,
            email=current_partner["email"],
            stage=request.stage,
            reason=request.reason,
        )
    )

# =========================================================
# PHOTO UPLOAD
# =========================================================


@router.post(
    "/bookings/{booking_id}/photos"
)
async def upload_photo(
    booking_id: str,
    stage: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...),
    current_partner=Depends(
        get_current_partner
    ),
):

    # ---------------------------------------------------------
    # VALIDATE PHOTO STAGE
    # ---------------------------------------------------------

    if stage not in (
        "before",
        "after",
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid photo stage.",
        )

    # ---------------------------------------------------------
    # VERIFY BOOKING BELONGS TO PARTNER
    # ---------------------------------------------------------

    booking = (
        PartnerBookingRepository
        .get_booking_for_partner(
            booking_id=booking_id,
            email=current_partner["email"],
        )
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found.",
        )

    # ---------------------------------------------------------
    # VERIFY BOOKING IS ACTIVE
    # ---------------------------------------------------------

    work_status = str(
        booking.get("work_status") or ""
    ).strip().upper()

    if work_status in (
        "COMPLETED",
        "CANCELLED",
    ):
        raise HTTPException(
            status_code=409,
            detail="This booking is no longer active.",
        )

    # ---------------------------------------------------------
    # READ FILE
    # ---------------------------------------------------------

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # ---------------------------------------------------------
    # SAVE PHOTO THROUGH REPOSITORY
    # ---------------------------------------------------------

    try:

        result = (
            PartnerBookingRepository
            .save_photo(
                booking=booking,
                email=current_partner["email"],
                stage=stage,
                category=category,
                file_bytes=file_bytes,
                content_type=(
                    file.content_type
                    or "image/jpeg"
                ),
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            "PHOTO UPLOAD ERROR:",
            repr(error),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Photo upload failed: {str(error)}"
            ),
        )

    # ---------------------------------------------------------
    # RESPONSE
    # ---------------------------------------------------------

    return {
        "success": True,
        "message": "Photo uploaded successfully.",
        "data": result,
    }

# =========================================================
# UPDATE PUSH TOKEN
# =========================================================

@router.patch("/push-token")
async def update_push_token(
    request: PushTokenRequest,
    current_partner=Depends(get_current_partner),
):
    partner_id = str(current_partner["id"])

    response = (
        supabase_admin
        .table("staff_profile")
        .update({
            "push_token": request.push_token,
        })
        .eq("id", partner_id)
        .execute()
    )

    return {
        "success": True,
        "message": "Push token updated successfully.",
        "data": response.data,
    }
# =========================================================
# NOTIFICATIONS
# =========================================================

@router.get("/notifications")
async def get_notifications(
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerNotificationService.get_notifications(
        staff_email=staff_email,
    )


@router.patch("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerNotificationService.mark_as_read(
        notification_id=notification_id,
        staff_email=staff_email,
    )


@router.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerNotificationService.delete_notification(
        notification_id=notification_id,
        staff_email=staff_email,
    )


@router.delete("/notifications")
async def delete_all_notifications(
    current_partner=Depends(get_current_partner),
):
    staff_email = current_partner["email"]

    return PartnerNotificationService.delete_all_notifications(
        staff_email=staff_email,
    )

# =========================================================
# HERO IMAGES
# =========================================================

@router.get("/hero-images")
async def get_hero_images(
    current_partner=Depends(get_current_partner),
):
    return PartnerHeroService.get_hero_images()


# =========================================================
# PARTNER AVAILABILITY
# =========================================================
@router.get("/availability")
async def get_my_availability(
    month: str = Query(...),
    current_partner=Depends(get_current_partner),
):
    return AvailabilityService.get_availability(
        email=current_partner["email"],
        month=month,
    )


@router.post("/availability")
async def save_my_availability(
    payload: AvailabilitySaveRequest,
    current_partner=Depends(get_current_partner),
):
    return AvailabilityService.save_availability(
        email=current_partner["email"],
        month=payload.month,
        calendar_data=payload.calendar_data,
    )