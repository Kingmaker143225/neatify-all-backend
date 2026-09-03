# from fastapi import HTTPException

# from app.repositories.partner_booking_repository import (
#     PartnerBookingRepository,
# )


# class PartnerBookingService:

#     ALLOWED_STATUSES = {
#         "pending",
#         "assigned",
#         "completed",
#         "cancelled",
#     }

#     @staticmethod
#     def get_bookings(
#         email: str,
#         status: str | None = None,
#     ):

#         normalized_status = None

#         if status:
#             normalized_status = status.strip().lower()

#             if normalized_status not in PartnerBookingService.ALLOWED_STATUSES:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Invalid booking status. "
#                         "Allowed values: pending, assigned, "
#                         "completed, cancelled."
#                     ),
#                 )

#         return PartnerBookingRepository.get_bookings(
#             email=email,
#             status=normalized_status,
#         )



















# from datetime import datetime, timezone

# from fastapi import HTTPException, status

# from app.repositories.partner_booking_repository import (
#     PartnerBookingRepository,
# )


# class PartnerBookingService:

#     ALLOWED_STATUSES = {
#         "pending",
#         "assigned",
#         "completed",
#         "cancelled",
#     }

#     # =========================================================
#     # GET BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_bookings(
#         email: str,
#         status: str | None = None,
#     ):

#         normalized_status = None

#         if status:
#             normalized_status = status.strip().lower()

#             if normalized_status not in PartnerBookingService.ALLOWED_STATUSES:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Invalid booking status. "
#                         "Allowed values: pending, assigned, "
#                         "completed, cancelled."
#                     ),
#                 )

#         return PartnerBookingRepository.get_bookings(
#             email=email,
#             status=normalized_status,
#         )

#     # =========================================================
#     # GET BOOKING DETAILS
#     # =========================================================

#     @staticmethod
#     def get_booking_details(
#         booking_id: str,
#         email: str,
#     ):

#         result = (
#             PartnerBookingRepository
#             .get_booking_details(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not result:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Booking not found.",
#             )

#         return {
#             "success": True,
#             "data": result,
#         }

#     # =========================================================
#     # START WORK
#     # =========================================================

#     @staticmethod
#     def start_work(
#         booking_id: str,
#         email: str,
#         start_otp: str,
#     ):

#         booking = (
#             PartnerBookingRepository
#             .get_booking_for_partner(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not booking:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Booking not found.",
#             )

#         if booking.get("work_status") in (
#             "COMPLETED",
#             "CANCELLED",
#         ):
#             raise HTTPException(
#                 status_code=409,
#                 detail="This booking is no longer active.",
#             )

#         expected_otp = str(
#             booking.get("startotp") or ""
#         ).strip()

#         if str(start_otp).strip() != expected_otp:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid Start OTP.",
#             )

#         if booking.get("work_started_at"):
#             raise HTTPException(
#                 status_code=409,
#                 detail="Work has already been started.",
#             )

#         start_time = datetime.now(
#             timezone.utc
#         ).isoformat()

#         result = (
#             PartnerBookingRepository
#             .start_work(
#                 booking_id=booking_id,
#                 email=email,
#                 start_time=start_time,
#             )
#         )

#         if not result:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Failed to start work.",
#             )

#         return {
#             "success": True,
#             "message": "Work started successfully.",
#             "booking_id": booking_id,
#             "work_started_at": start_time,
#         }

#     # =========================================================
#     # COMPLETE WORK
#     # =========================================================

#     @staticmethod
#     def complete_work(
#         booking_id: str,
#         email: str,
#         end_otp: str,
#         worked_duration: str,
#         staff_amount: float,
#     ):

#         booking = (
#             PartnerBookingRepository
#             .get_booking_for_partner(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not booking:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Booking not found.",
#             )

#         if booking.get("work_status") == "COMPLETED":
#             raise HTTPException(
#                 status_code=409,
#                 detail="This service is already completed.",
#             )

#         if booking.get("work_status") == "CANCELLED":
#             raise HTTPException(
#                 status_code=409,
#                 detail="This booking is cancelled.",
#             )

#         if not booking.get("work_started_at"):
#             raise HTTPException(
#                 status_code=409,
#                 detail="Work has not been started.",
#             )

#         expected_otp = str(
#             booking.get("endotp") or ""
#         ).strip()

#         if str(end_otp).strip() != expected_otp:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid End OTP.",
#             )

#         end_time = datetime.now(
#             timezone.utc
#         ).isoformat()

#         result = (
#             PartnerBookingRepository
#             .complete_work(
#                 booking_id=booking_id,
#                 email=email,
#                 worked_duration=worked_duration,
#                 staff_amount=float(staff_amount),
#                 end_time=end_time,
#             )
#         )

#         if not result:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Failed to complete service.",
#             )

#         # -----------------------------------------------------
#         # STAFF EARNINGS
#         # -----------------------------------------------------

#         try:
#             awaitable = None

#             PartnerBookingRepository.insert_staff_earning(
#                 booking=booking,
#                 amount=float(staff_amount),
#             )

#         except Exception as error:
#             print(
#                 "STAFF EARNINGS ERROR:",
#                 error,
#             )

#         # -----------------------------------------------------
#         # COMPLETED COUNT
#         # -----------------------------------------------------

#         try:
#             PartnerBookingRepository.update_completed_count(
#                 email=email,
#             )

#         except Exception as error:
#             print(
#                 "COMPLETED COUNT ERROR:",
#                 error,
#             )

#         return {
#             "success": True,
#             "message": "Service completed successfully.",
#             "booking_id": booking_id,
#             "amount": float(staff_amount),
#             "work_ended_at": end_time,
#         }

#     # =========================================================
#     # SKIP PHOTO
#     # =========================================================

#     @staticmethod
#     def skip_photo(
#         booking_id: str,
#         email: str,
#         stage: str,
#         reason: str,
#     ):

#         if not reason.strip():
#             raise HTTPException(
#                 status_code=400,
#                 detail="Skip reason is required.",
#             )

#         try:
#             result = (
#                 PartnerBookingRepository
#                 .skip_photo(
#                     booking_id=booking_id,
#                     email=email,
#                     stage=stage,
#                     reason=reason,
#                 )
#             )

#         except ValueError as error:
#             raise HTTPException(
#                 status_code=400,
#                 detail=str(error),
#             )

#         if not result:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Booking not found.",
#             )

#         return {
#             "success": True,
#             "message": "Photo skip reason saved.",
#             "stage": stage,
#             "reason": reason,
#         }













# from datetime import datetime, timezone

# from fastapi import HTTPException, status

# from app.repositories.partner_booking_repository import (
#     PartnerBookingRepository,
# )


# class PartnerBookingService:

#     ALLOWED_STATUSES = {
#         "pending",
#         "assigned",
#         "completed",
#         "cancelled",
#     }

#     # =========================================================
#     # GET BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_bookings(
#         email: str,
#         status: str | None = None,
#     ):

#         normalized_status = None

#         if status:

#             normalized_status = (
#                 status.strip().lower()
#             )

#             if (
#                 normalized_status
#                 not in PartnerBookingService.ALLOWED_STATUSES
#             ):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Invalid booking status. "
#                         "Allowed values: pending, assigned, "
#                         "completed, cancelled."
#                     ),
#                 )

#         return (
#             PartnerBookingRepository
#             .get_bookings(
#                 email=email,
#                 status=normalized_status,
#             )
#         )

#     # =========================================================
#     # GET BOOKING DETAILS
#     # =========================================================

#     @staticmethod
#     def get_booking_details(
#         booking_id: str,
#         email: str,
#     ):

#         result = (
#             PartnerBookingRepository
#             .get_booking_details(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not result:

#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Booking not found.",
#             )

#         return {
#             "success": True,
#             "data": result,
#         }

#     # =========================================================
#     # START WORK
#     # =========================================================

#     @staticmethod
#     def start_work(
#         booking_id: str,
#         email: str,
#         start_otp: str,
#     ):

#         booking = (
#             PartnerBookingRepository
#             .get_booking_for_partner(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not booking:

#             raise HTTPException(
#                 status_code=404,
#                 detail="Booking not found.",
#             )

#         # -----------------------------------------------------
#         # MUST BE APPROVED
#         # -----------------------------------------------------

#         if (
#             str(
#                 booking.get("staff_response")
#                 or ""
#             )
#             .strip()
#             .upper()
#             != "APPROVED"
#         ):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Booking has not been approved "
#                     "by the partner."
#                 ),
#             )

#         # -----------------------------------------------------
#         # MUST BE ASSIGNED
#         # -----------------------------------------------------

#         if (
#             str(
#                 booking.get("work_status")
#                 or ""
#             )
#             .strip()
#             .upper()
#             != "ASSIGNED"
#         ):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Booking is not in assigned state."
#                 ),
#             )

#         # -----------------------------------------------------
#         # ALREADY STARTED
#         # -----------------------------------------------------

#         if booking.get("work_started_at"):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Work has already been started."
#                 ),
#             )

#         # -----------------------------------------------------
#         # START OTP
#         # -----------------------------------------------------

#         expected_otp = str(
#             booking.get("startotp")
#             or ""
#         ).strip()

#         if (
#             str(start_otp).strip()
#             != expected_otp
#         ):

#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid Start OTP.",
#             )

#         # -----------------------------------------------------
#         # BEFORE PHOTOS / SKIP
#         # -----------------------------------------------------

#         uploads = (
#             PartnerBookingRepository
#             .get_service_uploads(
#                 booking_id=booking_id
#             )
#         )

#         before_uploads = (
#             uploads.get("before")
#             if isinstance(
#                 uploads,
#                 dict,
#             )
#             else {}
#         )

#         before_uploads = (
#             before_uploads
#             if isinstance(
#                 before_uploads,
#                 dict,
#             )
#             else {}
#         )

#         skipped_before = str(
#             booking.get(
#                 "start_photo_url"
#             )
#             or ""
#         ).startswith("Skipped:")

#         if (
#             not before_uploads
#             and not skipped_before
#         ):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Before photos are required "
#                     "before starting work."
#                 ),
#             )

#         # -----------------------------------------------------
#         # START TIME
#         # -----------------------------------------------------

#         start_time = (
#             datetime.now(
#                 timezone.utc
#             ).isoformat()
#         )

#         result = (
#             PartnerBookingRepository
#             .start_work(
#                 booking_id=booking_id,
#                 email=email,
#                 start_time=start_time,
#             )
#         )

#         if not result:

#             raise HTTPException(
#                 status_code=500,
#                 detail="Failed to start work.",
#             )

#         return {
#             "success": True,
#             "message": (
#                 "Work started successfully."
#             ),
#             "booking_id": booking_id,
#             "work_started_at": start_time,
#         }

#     # =========================================================
#     # COMPLETE WORK
#     # =========================================================

#     @staticmethod
#     def complete_work(
#         booking_id: str,
#         email: str,
#         end_otp: str,
#         worked_duration: str,
#         staff_amount: float,
#     ):

#         booking = (
#             PartnerBookingRepository
#             .get_booking_for_partner(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not booking:

#             raise HTTPException(
#                 status_code=404,
#                 detail="Booking not found.",
#             )

#         # -----------------------------------------------------
#         # APPROVED
#         # -----------------------------------------------------

#         if (
#             str(
#                 booking.get("staff_response")
#                 or ""
#             )
#             .strip()
#             .upper()
#             != "APPROVED"
#         ):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Booking has not been approved."
#                 ),
#             )

#         # -----------------------------------------------------
#         # STATUS
#         # -----------------------------------------------------

#         work_status = str(
#             booking.get("work_status")
#             or ""
#         ).strip().upper()

#         if work_status == "COMPLETED":

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "This service is already completed."
#                 ),
#             )

#         if work_status == "CANCELLED":

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "This booking is cancelled."
#                 ),
#             )

#         if work_status != "ASSIGNED":

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Booking is not in assigned state."
#                 ),
#             )

#         # -----------------------------------------------------
#         # WORK MUST HAVE STARTED
#         # -----------------------------------------------------

#         if not booking.get(
#             "work_started_at"
#         ):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "Work has not been started."
#                 ),
#             )

#         # -----------------------------------------------------
#         # AFTER PHOTOS / SKIP
#         # -----------------------------------------------------

#         uploads = (
#             PartnerBookingRepository
#             .get_service_uploads(
#                 booking_id=booking_id
#             )
#         )

#         after_uploads = (
#             uploads.get("after")
#             if isinstance(
#                 uploads,
#                 dict,
#             )
#             else {}
#         )

#         after_uploads = (
#             after_uploads
#             if isinstance(
#                 after_uploads,
#                 dict,
#             )
#             else {}
#         )

#         skipped_after = str(
#             booking.get(
#                 "end_photo_url"
#             )
#             or ""
#         ).startswith("Skipped:")

#         if (
#             not after_uploads
#             and not skipped_after
#         ):

#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "After photos are required "
#                     "before completing the service."
#                 ),
#             )

#         # -----------------------------------------------------
#         # END OTP
#         # -----------------------------------------------------

#         expected_otp = str(
#             booking.get("endotp")
#             or ""
#         ).strip()

#         if (
#             str(end_otp).strip()
#             != expected_otp
#         ):

#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid End OTP.",
#             )

#         # -----------------------------------------------------
#         # END TIME
#         # -----------------------------------------------------

#         end_time = (
#             datetime.now(
#                 timezone.utc
#             ).isoformat()
#         )

#         # -----------------------------------------------------
#         # COMPLETE BOOKING
#         # -----------------------------------------------------

#         result = (
#             PartnerBookingRepository
#             .complete_work(
#                 booking_id=booking_id,
#                 email=email,
#                 worked_duration=worked_duration,
#                 staff_amount=float(
#                     staff_amount
#                 ),
#                 end_time=end_time,
#             )
#         )

#         if not result:

#             raise HTTPException(
#                 status_code=500,
#                 detail=(
#                     "Failed to complete service."
#                 ),
#             )

#         # -----------------------------------------------------
#         # STAFF EARNINGS
#         # -----------------------------------------------------

#         try:

#             PartnerBookingRepository \
#                 .insert_staff_earning(
#                     booking=booking,
#                     amount=float(
#                         staff_amount
#                     ),
#                 )

#         except Exception as error:

#             print(
#                 "STAFF EARNINGS ERROR:",
#                 error,
#             )

#         # -----------------------------------------------------
#         # COMPLETED COUNT
#         # -----------------------------------------------------

#         try:

#             PartnerBookingRepository \
#                 .update_completed_count(
#                     email=email,
#                 )

#         except Exception as error:

#             print(
#                 "COMPLETED COUNT ERROR:",
#                 error,
#             )

#         return {
#             "success": True,
#             "message": (
#                 "Service completed successfully."
#             ),
#             "booking_id": booking_id,
#             "amount": float(
#                 staff_amount
#             ),
#             "work_ended_at": end_time,
#         }

#     # # =========================================================
#     # # SKIP PHOTO
#     # # =========================================================

#     # @staticmethod
#     # def skip_photo(
#     #     booking_id: str,
#     #     email: str,
#     #     stage: str,
#     #     reason: str,
#     # ):

#     #     if stage not in (
#     #         "start",
#     #         "end",
#     #     ):

#     #         raise HTTPException(
#     #             status_code=400,
#     #             detail="Invalid photo stage.",
#     #         )

#     #     if not reason.strip():

#     #         raise HTTPException(
#     #             status_code=400,
#     #             detail="Skip reason is required.",
#     #         )

#     #     # -----------------------------------------------------
#     #     # VERIFY BOOKING
#     #     # -----------------------------------------------------

#     #     booking = (
#     #         PartnerBookingRepository
#     #         .get_booking_for_partner(
#     #             booking_id=booking_id,
#     #             email=email,
#     #         )
#     #     )

#     #     if not booking:

#     #         raise HTTPException(
#     #             status_code=404,
#     #             detail="Booking not found.",
#     #         )

#     #     work_status = str(
#     #         booking.get("work_status")
#     #         or ""
#     #     ).strip().upper()

#     #     if work_status in (
#     #         "COMPLETED",
#     #         "CANCELLED",
#     #     ):

#     #         raise HTTPException(
#     #             status_code=409,
#     #             detail=(
#     #                 "This booking is no longer active."
#     #             ),
#     #         )

#     #     try:

#     #         result = (
#     #             PartnerBookingRepository
#     #             .skip_photo(
#     #                 booking_id=booking_id,
#     #                 email=email,
#     #                 stage=stage,
#     #                 reason=reason,
#     #             )
#     #         )

#     #     except ValueError as error:

#     #         raise HTTPException(
#     #             status_code=400,
#     #             detail=str(error),
#     #         )

#     #     if not result:

#     #         raise HTTPException(
#     #             status_code=404,
#     #             detail="Booking not found.",
#     #         )

#     #     return {
#     #         "success": True,
#     #         "message": (
#     #             "Photo skip reason saved."
#     #         ),
#     #         "stage": stage,
#     #         "reason": reason,
#     #     }
#     # =========================================================
#     # SKIP PHOTO
#     # =========================================================

#     @staticmethod
#     def skip_photo(
#         booking_id: str,
#         email: str,
#         stage: str,
#         reason: str,
#     ):

#         # -----------------------------------------------------
#         # NORMALIZE STAGE
#         # -----------------------------------------------------

#         normalized_stage = (
#             str(stage or "")
#             .strip()
#             .lower()
#         )

#         if normalized_stage not in (
#             "before",
#             "after",
#         ):
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Invalid photo stage. "
#                     "Allowed values: before, after."
#                 ),
#             )

#         # -----------------------------------------------------
#         # VALIDATE REASON
#         # -----------------------------------------------------

#         normalized_reason = (
#             str(reason or "")
#             .strip()
#         )

#         if not normalized_reason:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Skip reason is required.",
#             )

#         # -----------------------------------------------------
#         # VERIFY BOOKING
#         # -----------------------------------------------------

#         booking = (
#             PartnerBookingRepository
#             .get_booking_for_partner(
#                 booking_id=booking_id,
#                 email=email,
#             )
#         )

#         if not booking:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Booking not found.",
#             )

#         # -----------------------------------------------------
#         # BOOKING STATUS
#         # -----------------------------------------------------

#         work_status = str(
#             booking.get("work_status") or ""
#         ).strip().upper()

#         if work_status in (
#             "COMPLETED",
#             "CANCELLED",
#         ):
#             raise HTTPException(
#                 status_code=409,
#                 detail=(
#                     "This booking is no longer active."
#                 ),
#             )

#         # -----------------------------------------------------
#         # SAVE SKIP
#         # -----------------------------------------------------

#         try:

#             result = (
#                 PartnerBookingRepository
#                 .skip_photo(
#                     booking_id=booking_id,
#                     email=email,
#                     stage=normalized_stage,
#                     reason=normalized_reason,
#                 )
#             )

#         except ValueError as error:

#             raise HTTPException(
#                 status_code=400,
#                 detail=str(error),
#             )

#         # -----------------------------------------------------
#         # VERIFY RESULT
#         # -----------------------------------------------------

#         if not result:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Failed to save photo skip reason.",
#             )

#         # -----------------------------------------------------
#         # RESPONSE
#         # -----------------------------------------------------

#         return {
#             "success": True,
#             "message": "Photo skip reason saved.",
#             "booking_id": booking_id,
#             "stage": normalized_stage,
#             "reason": normalized_reason,
#         }
















from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.partner_booking_repository import (
    PartnerBookingRepository,
)


class PartnerBookingService:

    ALLOWED_STATUSES = {
        "pending",
        "assigned",
        "completed",
        "cancelled",
    }

    # =========================================================
    # GET BOOKINGS
    # =========================================================

    @staticmethod
    def get_bookings(
        email: str,
        status: str | None = None,
    ):

        normalized_status = None

        if status:

            normalized_status = (
                status.strip().lower()
            )

            if (
                normalized_status
                not in PartnerBookingService.ALLOWED_STATUSES
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Invalid booking status. "
                        "Allowed values: pending, assigned, "
                        "completed, cancelled."
                    ),
                )

        return (
            PartnerBookingRepository
            .get_bookings(
                email=email,
                status=normalized_status,
            )
        )

    # =========================================================
    # GET BOOKING DETAILS
    # =========================================================

    @staticmethod
    def get_booking_details(
        booking_id: str,
        email: str,
    ):

        result = (
            PartnerBookingRepository
            .get_booking_details(
                booking_id=booking_id,
                email=email,
            )
        )

        if not result:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found.",
            )

        return {
            "success": True,
            "data": result,
        }

    # =========================================================
    # START WORK
    # =========================================================

    @staticmethod
    def start_work(
        booking_id: str,
        email: str,
        start_otp: str,
    ):

        booking = (
            PartnerBookingRepository
            .get_booking_for_partner(
                booking_id=booking_id,
                email=email,
            )
        )

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found.",
            )

        # -----------------------------------------------------
        # MUST BE APPROVED
        # -----------------------------------------------------

        # if (
        #     str(
        #         booking.get("staff_response")
        #         or ""
        #     )
        #     .strip()
        #     .upper()
        #     != "APPROVED"
        # ):

        #     raise HTTPException(
        #         status_code=409,
        #         detail=(
        #             "Booking has not been approved "
        #             "by the partner."
        #         ),
        #     )

        # -----------------------------------------------------
        # MUST BE ASSIGNED
        # -----------------------------------------------------

        # if (
        #     str(
        #         booking.get("work_status")
        #         or ""
        #     )
        #     .strip()
        #     .upper()
        #     != "ASSIGNED"
        # ):

        #     raise HTTPException(
        #         status_code=409,
        #         detail=(
        #             "Booking is not in assigned state."
        #         ),
        #     )
        # -----------------------------------------------------
        # MUST BE ASSIGNED
        # -----------------------------------------------------

        if (
            str(
                booking.get("work_status")
                or ""
            )
            .strip()
            .upper()
            != "ASSIGNED"
        ):
            raise HTTPException(
                status_code=409,
                detail="Booking is not in assigned state.",
            )
        # -----------------------------------------------------
        # ALREADY STARTED
        # -----------------------------------------------------

        if booking.get("work_started_at"):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Work has already been started."
                ),
            )

        # -----------------------------------------------------
        # START OTP
        # -----------------------------------------------------

        expected_otp = str(
            booking.get("startotp")
            or ""
        ).strip()

        if (
            str(start_otp).strip()
            != expected_otp
        ):

            raise HTTPException(
                status_code=400,
                detail="Invalid Start OTP.",
            )

        # -----------------------------------------------------
        # BEFORE PHOTOS / SKIP
        # -----------------------------------------------------

        uploads = (
            PartnerBookingRepository
            .get_service_uploads(
                booking_id=booking_id
            )
        )

        before_uploads = (
            uploads.get("before")
            if isinstance(
                uploads,
                dict,
            )
            else {}
        )

        before_uploads = (
            before_uploads
            if isinstance(
                before_uploads,
                dict,
            )
            else {}
        )

        skipped_before = str(
            booking.get(
                "start_photo_url"
            )
            or ""
        ).startswith("Skipped:")

        if (
            not before_uploads
            and not skipped_before
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Before photos are required "
                    "before starting work."
                ),
            )

        # -----------------------------------------------------
        # START TIME
        # -----------------------------------------------------

        start_time = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        result = (
            PartnerBookingRepository
            .start_work(
                booking_id=booking_id,
                email=email,
                start_time=start_time,
            )
        )

        if not result:

            raise HTTPException(
                status_code=500,
                detail="Failed to start work.",
            )

        return {
            "success": True,
            "message": (
                "Work started successfully."
            ),
            "booking_id": booking_id,
            "work_started_at": start_time,
        }

    # =========================================================
    # COMPLETE WORK
    # =========================================================

    @staticmethod
    def complete_work(
        booking_id: str,
        email: str,
        end_otp: str,
        worked_duration: str,
        staff_amount: float,
    ):

        booking = (
            PartnerBookingRepository
            .get_booking_for_partner(
                booking_id=booking_id,
                email=email,
            )
        )

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found.",
            )

        # -----------------------------------------------------
        # APPROVED
        # -----------------------------------------------------

        # if (
        #     str(
        #         booking.get("staff_response")
        #         or ""
        #     )
        #     .strip()
        #     .upper()
        #     != "APPROVED"
        # ):

        #     raise HTTPException(
        #         status_code=409,
        #         detail=(
        #             "Booking has not been approved."
        #         ),
        #     )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        work_status = str(
            booking.get("work_status")
            or ""
        ).strip().upper()

        if work_status == "COMPLETED":

            raise HTTPException(
                status_code=409,
                detail=(
                    "This service is already completed."
                ),
            )

        if work_status == "CANCELLED":

            raise HTTPException(
                status_code=409,
                detail=(
                    "This booking is cancelled."
                ),
            )

        if work_status != "ASSIGNED":

            raise HTTPException(
                status_code=409,
                detail=(
                    "Booking is not in assigned state."
                ),
            )

        # -----------------------------------------------------
        # WORK MUST HAVE STARTED
        # -----------------------------------------------------

        if not booking.get(
            "work_started_at"
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Work has not been started."
                ),
            )

        # -----------------------------------------------------
        # AFTER PHOTOS / SKIP
        # -----------------------------------------------------

        uploads = (
            PartnerBookingRepository
            .get_service_uploads(
                booking_id=booking_id
            )
        )

        after_uploads = (
            uploads.get("after")
            if isinstance(
                uploads,
                dict,
            )
            else {}
        )

        after_uploads = (
            after_uploads
            if isinstance(
                after_uploads,
                dict,
            )
            else {}
        )

        skipped_after = str(
            booking.get(
                "end_photo_url"
            )
            or ""
        ).startswith("Skipped:")

        if (
            not after_uploads
            and not skipped_after
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "After photos are required "
                    "before completing the service."
                ),
            )

        # -----------------------------------------------------
        # END OTP
        # -----------------------------------------------------

        expected_otp = str(
            booking.get("endotp")
            or ""
        ).strip()

        if (
            str(end_otp).strip()
            != expected_otp
        ):

            raise HTTPException(
                status_code=400,
                detail="Invalid End OTP.",
            )

        # -----------------------------------------------------
        # END TIME
        # -----------------------------------------------------

        end_time = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        # -----------------------------------------------------
        # COMPLETE BOOKING
        # -----------------------------------------------------

        result = (
            PartnerBookingRepository
            .complete_work(
                booking_id=booking_id,
                email=email,
                worked_duration=worked_duration,
                staff_amount=float(
                    staff_amount
                ),
                end_time=end_time,
            )
        )

        if not result:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to complete service."
                ),
            )

        # -----------------------------------------------------
        # STAFF EARNINGS
        # -----------------------------------------------------

        try:

            PartnerBookingRepository \
                .insert_staff_earning(
                    booking=booking,
                    amount=float(
                        staff_amount
                    ),
                )

        except Exception as error:

            print(
                "STAFF EARNINGS ERROR:",
                error,
            )

        # -----------------------------------------------------
        # COMPLETED COUNT
        # -----------------------------------------------------

        try:

            PartnerBookingRepository \
                .update_completed_count(
                    email=email,
                )

        except Exception as error:

            print(
                "COMPLETED COUNT ERROR:",
                error,
            )

        return {
            "success": True,
            "message": (
                "Service completed successfully."
            ),
            "booking_id": booking_id,
            "amount": float(
                staff_amount
            ),
            "work_ended_at": end_time,
        }

    # # =========================================================
    # # SKIP PHOTO
    # # =========================================================

    # @staticmethod
    # def skip_photo(
    #     booking_id: str,
    #     email: str,
    #     stage: str,
    #     reason: str,
    # ):

    #     if stage not in (
    #         "start",
    #         "end",
    #     ):

    #         raise HTTPException(
    #             status_code=400,
    #             detail="Invalid photo stage.",
    #         )

    #     if not reason.strip():

    #         raise HTTPException(
    #             status_code=400,
    #             detail="Skip reason is required.",
    #         )

    #     # -----------------------------------------------------
    #     # VERIFY BOOKING
    #     # -----------------------------------------------------

    #     booking = (
    #         PartnerBookingRepository
    #         .get_booking_for_partner(
    #             booking_id=booking_id,
    #             email=email,
    #         )
    #     )

    #     if not booking:

    #         raise HTTPException(
    #             status_code=404,
    #             detail="Booking not found.",
    #         )

    #     work_status = str(
    #         booking.get("work_status")
    #         or ""
    #     ).strip().upper()

    #     if work_status in (
    #         "COMPLETED",
    #         "CANCELLED",
    #     ):

    #         raise HTTPException(
    #             status_code=409,
    #             detail=(
    #                 "This booking is no longer active."
    #             ),
    #         )

    #     try:

    #         result = (
    #             PartnerBookingRepository
    #             .skip_photo(
    #                 booking_id=booking_id,
    #                 email=email,
    #                 stage=stage,
    #                 reason=reason,
    #             )
    #         )

    #     except ValueError as error:

    #         raise HTTPException(
    #             status_code=400,
    #             detail=str(error),
    #         )

    #     if not result:

    #         raise HTTPException(
    #             status_code=404,
    #             detail="Booking not found.",
    #         )

    #     return {
    #         "success": True,
    #         "message": (
    #             "Photo skip reason saved."
    #         ),
    #         "stage": stage,
    #         "reason": reason,
    #     }
    # =========================================================
    # SKIP PHOTO
    # =========================================================

    @staticmethod
    def skip_photo(
        booking_id: str,
        email: str,
        stage: str,
        reason: str,
    ):

        # -----------------------------------------------------
        # NORMALIZE STAGE
        # -----------------------------------------------------

        normalized_stage = (
            str(stage or "")
            .strip()
            .lower()
        )

        if normalized_stage not in (
            "before",
            "after",
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid photo stage. "
                    "Allowed values: before, after."
                ),
            )

        # -----------------------------------------------------
        # VALIDATE REASON
        # -----------------------------------------------------

        normalized_reason = (
            str(reason or "")
            .strip()
        )

        if not normalized_reason:
            raise HTTPException(
                status_code=400,
                detail="Skip reason is required.",
            )

        # -----------------------------------------------------
        # VERIFY BOOKING
        # -----------------------------------------------------

        booking = (
            PartnerBookingRepository
            .get_booking_for_partner(
                booking_id=booking_id,
                email=email,
            )
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found.",
            )

        # -----------------------------------------------------
        # BOOKING STATUS
        # -----------------------------------------------------

        work_status = str(
            booking.get("work_status") or ""
        ).strip().upper()

        if work_status in (
            "COMPLETED",
            "CANCELLED",
        ):
            raise HTTPException(
                status_code=409,
                detail=(
                    "This booking is no longer active."
                ),
            )

        # -----------------------------------------------------
        # SAVE SKIP
        # -----------------------------------------------------

        try:

            result = (
                PartnerBookingRepository
                .skip_photo(
                    booking_id=booking_id,
                    email=email,
                    stage=normalized_stage,
                    reason=normalized_reason,
                )
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

        # -----------------------------------------------------
        # VERIFY RESULT
        # -----------------------------------------------------

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to save photo skip reason.",
            )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        return {
            "success": True,
            "message": "Photo skip reason saved.",
            "booking_id": booking_id,
            "stage": normalized_stage,
            "reason": normalized_reason,
        }