# from app.supabase.client import supabase


# class PartnerBookingRepository:

#     @staticmethod
#     def get_bookings(email: str, status: str | None = None):

#         query = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("assigned_staff_email", email)
#         )

#         if status == "pending":
#             # Pending means the partner has not responded yet.
#             query = query.or_(
#                 "staff_response.is.null,staff_response.eq.pending"
#             )

#         elif status == "assigned":
#             # Active bookings.
#             query = (
#                 query
#                 .neq("work_status", "COMPLETED")
#                 .neq("work_status", "CANCELLED")
#             )

#         elif status == "completed":
#             query = query.eq("work_status", "COMPLETED")

#         elif status == "cancelled":
#             query = query.eq("work_status", "CANCELLED")

#         response = (
#             query
#             .order("booking_date", desc=True)
#             .execute()
#         )

#         return response.data or []

#     @staticmethod
#     def get_booking_for_partner(
#         booking_id: str,
#         email: str,
#     ):
#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         return response.data


#     @staticmethod
#     def approve_booking(
#         booking_id: str,
#         email: str,
#     ):
#         response = (
#             supabase
#             .table("bookings")
#             .update({
#                 "staff_response": "APPROVED",
#                 "work_status": "ASSIGNED",
#             })
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data


#     @staticmethod
#     def reject_booking(
#         booking_id: str,
#         email: str,
#         reason: str,
#     ):
#         response = (
#             supabase
#             .table("bookings")
#             .update({
#                 "staff_response": "REJECTED",
#                 "reject_reason": reason,
#             })
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data










# from app.supabase.client import supabase


# class PartnerBookingRepository:

#     @staticmethod
#     def get_bookings(
#         email: str,
#         status: str | None = None,
#     ):
#         """
#         Get bookings assigned to the authenticated partner.

#         Supported statuses:
#         - pending
#         - assigned
#         - completed
#         - cancelled
#         """

#         query = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("assigned_staff_email", email)
#         )

#         # ---------------------------------------------------------
#         # PENDING
#         # ---------------------------------------------------------
#         if status == "pending":
#             """
#             A booking is considered pending when:

#             1. It belongs to this partner
#             2. Partner has not responded yet
#                OR response is explicitly pending
#             3. Booking is not completed
#             4. Booking is not cancelled
#             """

#             query = (
#                 query
#                 .or_(
#                     "staff_response.is.null,staff_response.eq.pending"
#                 )
#                 .neq("work_status", "COMPLETED")
#                 .neq("work_status", "CANCELLED")
#             )

#         # ---------------------------------------------------------
#         # ASSIGNED
#         # ---------------------------------------------------------
#         elif status == "assigned":
#             """
#             Assigned/active booking means:

#             1. Partner approved it
#             2. It is not completed
#             3. It is not cancelled
#             """

#             query = (
#                 query
#                 .eq("staff_response", "APPROVED")
#                 .neq("work_status", "COMPLETED")
#                 .neq("work_status", "CANCELLED")
#             )

#         # ---------------------------------------------------------
#         # COMPLETED
#         # ---------------------------------------------------------
#         elif status == "completed":

#             query = query.eq(
#                 "work_status",
#                 "COMPLETED",
#             )

#         # ---------------------------------------------------------
#         # CANCELLED
#         # ---------------------------------------------------------
#         elif status == "cancelled":

#             query = query.eq(
#                 "work_status",
#                 "CANCELLED",
#             )

#         # ---------------------------------------------------------
#         # Execute query
#         # ---------------------------------------------------------

#         response = (
#             query
#             .order(
#                 "booking_date",
#                 desc=True,
#             )
#             .execute()
#         )

#         return response.data or []

#     # =============================================================
#     # GET SINGLE BOOKING FOR PARTNER
#     # =============================================================

#     @staticmethod
#     def get_booking_for_partner(
#         booking_id: str,
#         email: str,
#     ):
#         """
#         Get a single booking only if it belongs to this partner.
#         """

#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =============================================================
#     # APPROVE BOOKING
#     # =============================================================

#     @staticmethod
#     def approve_booking(
#         booking_id: str,
#         email: str,
#     ):
#         """
#         Approve a booking.

#         State after approval:

#         staff_response = APPROVED
#         work_status = ASSIGNED
#         """

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "staff_response": "APPROVED",
#                     "work_status": "ASSIGNED",
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =============================================================
#     # REJECT BOOKING
#     # =============================================================

#     @staticmethod
#     def reject_booking(
#         booking_id: str,
#         email: str,
#         reason: str,
#     ):
#         """
#         Reject a booking.

#         State after rejection:

#         staff_response = REJECTED
#         reject_reason = supplied reason
#         """

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "staff_response": "REJECTED",
#                     "reject_reason": reason,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data













# from datetime import datetime, timezone

# from app.supabase.client import supabase


# class PartnerBookingRepository:

#     # =========================================================
#     # GET BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_bookings(
#         email: str,
#         status: str | None = None,
#     ):

#         query = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("assigned_staff_email", email)
#         )

#         # -----------------------------------------------------
#         # PENDING
#         # -----------------------------------------------------

#         if status == "pending":

#             query = (
#                 query
#                 .or_(
#                     "staff_response.is.null,staff_response.eq.pending"
#                 )
#                 .neq("work_status", "COMPLETED")
#                 .neq("work_status", "CANCELLED")
#             )

#         # -----------------------------------------------------
#         # ASSIGNED
#         # -----------------------------------------------------

#         elif status == "assigned":

#             query = (
#                 query
#                 .eq("staff_response", "APPROVED")
#                 .neq("work_status", "COMPLETED")
#                 .neq("work_status", "CANCELLED")
#             )

#         # -----------------------------------------------------
#         # COMPLETED
#         # -----------------------------------------------------

#         elif status == "completed":

#             query = query.eq(
#                 "work_status",
#                 "COMPLETED",
#             )

#         # -----------------------------------------------------
#         # CANCELLED
#         # -----------------------------------------------------

#         elif status == "cancelled":

#             query = query.eq(
#                 "work_status",
#                 "CANCELLED",
#             )

#         # -----------------------------------------------------
#         # EXECUTE
#         # -----------------------------------------------------

#         response = (
#             query
#             .order(
#                 "booking_date",
#                 desc=True,
#             )
#             .execute()
#         )

#         return response.data or []

#     # =========================================================
#     # GET SINGLE BOOKING
#     # =========================================================

#     @staticmethod
#     def get_booking_for_partner(
#         booking_id: str,
#         email: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # GET BOOKING DETAILS
#     # =========================================================

#     @staticmethod
#     def get_booking_details(
#         booking_id: str,
#         email: str,
#     ):

#         booking_response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         booking = booking_response.data

#         if not booking:
#             return None

#         # -----------------------------------------------------
#         # SERVICE UPLOADS
#         # -----------------------------------------------------

#         uploads_response = (
#             supabase
#             .table("service_uploads")
#             .select("uploads")
#             .eq("booking_id", booking_id)
#             .maybe_single()
#             .execute()
#         )

#         uploads = (
#             uploads_response.data.get("uploads")
#             if uploads_response.data
#             else None
#         )

#         # -----------------------------------------------------
#         # SERVICE DETAILS
#         # -----------------------------------------------------

#         service_id = None

#         services = booking.get("services")

#         if isinstance(services, list) and services:

#             first_service = services[0]

#             if isinstance(first_service, dict):
#                 service_id = first_service.get("id")
#             else:
#                 service_id = first_service

#         service = None

#         if service_id:

#             service_response = (
#                 supabase
#                 .table("services")
#                 .select(
#                     "id, staff_amount, service_type"
#                 )
#                 .eq("id", service_id)
#                 .maybe_single()
#                 .execute()
#             )

#             service = service_response.data

#         # -----------------------------------------------------
#         # RESPONSE
#         # -----------------------------------------------------

#         return {
#             "booking": booking,
#             "uploads": uploads or {
#                 "before": {},
#                 "after": {},
#             },
#             "service": service or {},
#         }

#     # =========================================================
#     # APPROVE
#     # =========================================================

#     @staticmethod
#     def approve_booking(
#         booking_id: str,
#         email: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "staff_response": "APPROVED",
#                     "work_status": "ASSIGNED",
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # REJECT
#     # =========================================================

#     @staticmethod
#     def reject_booking(
#         booking_id: str,
#         email: str,
#         reason: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "staff_response": "REJECTED",
#                     "reject_reason": reason,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =============================================================
#     # CANCEL ASSIGNED BOOKING
#     # =============================================================

#     @staticmethod
#     def cancel_booking(
#         booking_id: str,
#         email: str,
#         reason: str,
#         cancellation_fee: float = 99,
#     ):
#         """
#         Cancel an assigned/approved booking.

#         Final database state:

#         staff_response      = APPROVED
#         work_status         = CANCELLED
#         cancel_reason       = selected reason
#         cancel_time         = current database timestamp
#         cancel_requested    = True
#         cancellation_fee    = 99
#         """

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "work_status": "CANCELLED",
#                     "cancel_reason": reason,
#                     "cancel_requested": True,
#                     "cancellation_fee": cancellation_fee,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .eq("staff_response", "APPROVED")
#             .eq("work_status", "ASSIGNED")
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # START WORK
#     # =========================================================

#     @staticmethod
#     def start_work(
#         booking_id: str,
#         email: str,
#         start_time: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "work_started_at": start_time,
#                     "work_status": "ASSIGNED",
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # COMPLETE WORK
#     # =========================================================

#     @staticmethod
#     def complete_work(
#         booking_id: str,
#         email: str,
#         worked_duration: str,
#         staff_amount: float,
#         end_time: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "work_status": "COMPLETED",
#                     "worked_duration": worked_duration,
#                     "staff_earned_amount": staff_amount,
#                     "work_ended_at": end_time,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # INSERT STAFF EARNINGS
#     # =========================================================

#     @staticmethod
#     def insert_staff_earning(
#         booking: dict,
#         amount: float,
#     ):

#         response = (
#             supabase
#             .table("staff_earnings")
#             .insert(
#                 {
#                     "booking_id": booking["id"],
#                     "staff_email": booking[
#                         "assigned_staff_email"
#                     ],
#                     "Customer_Name": booking[
#                         "customer_name"
#                     ],
#                     "AMOUNT": amount,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # UPDATE COMPLETED COUNT
#     # =========================================================

#     @staticmethod
#     def update_completed_count(
#         email: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .select(
#                 "id",
#                 count="exact",
#                 head=True,
#             )
#             .eq(
#                 "assigned_staff_email",
#                 email,
#             )
#             .eq(
#                 "work_status",
#                 "COMPLETED",
#             )
#             .execute()
#         )

#         completed_count = response.count or 0

#         profile_response = (
#             supabase
#             .table("staff_profile")
#             .update(
#                 {
#                     "total_completed": completed_count,
#                 }
#             )
#             .eq("email", email)
#             .execute()
#         )

#         return profile_response.data

#     # =========================================================
#     # SAVE PHOTO
#     # =========================================================

#     @staticmethod
#     def save_photo(
#         booking: dict,
#         email: str,
#         stage: str,
#         category: str,
#         file_bytes: bytes,
#         content_type: str = "image/jpeg",
#     ):

#         safe_customer_name = (
#             booking.get("customer_name", "customer")
#             .replace(" ", "_")
#         )

#         folder_name = (
#             f"{safe_customer_name}_({booking['id']})"
#         )

#         file_path = (
#             f"{email}/"
#             f"{folder_name}/"
#             f"{stage}/"
#             f"{category}.jpg"
#         )

#         # -----------------------------------------------------
#         # STORAGE UPLOAD
#         # -----------------------------------------------------

#         upload_response = (
#             supabase.storage
#             .from_("work_uploads")
#             .upload(
#                 file_path,
#                 file_bytes,
#                 {
#                     "content-type": content_type,
#                     "upsert": "true",
#                 },
#             )
#         )

#         # -----------------------------------------------------
#         # PUBLIC URL
#         # -----------------------------------------------------

#         public_data = (
#             supabase.storage
#             .from_("work_uploads")
#             .get_public_url(file_path)
#         )

#         image_url = public_data

#         if isinstance(public_data, dict):
#             image_url = public_data.get(
#                 "publicUrl"
#             ) or public_data.get(
#                 "public_url"
#             )

#         if not image_url:
#             raise Exception(
#                 "Unable to generate public image URL."
#             )

#         # -----------------------------------------------------
#         # EXISTING UPLOADS
#         # -----------------------------------------------------

#         existing_response = (
#             supabase
#             .table("service_uploads")
#             .select("uploads")
#             .eq("booking_id", booking["id"])
#             .maybe_single()
#             .execute()
#         )

#         uploads = (
#             existing_response.data.get("uploads")
#             if existing_response.data
#             else None
#         )

#         if not uploads:
#             uploads = {
#                 "before": {},
#                 "after": {},
#             }

#         if "before" not in uploads:
#             uploads["before"] = {}

#         if "after" not in uploads:
#             uploads["after"] = {}

#         uploads[stage][category] = image_url

#         # -----------------------------------------------------
#         # UPSERT
#         # -----------------------------------------------------

#         db_response = (
#             supabase
#             .table("service_uploads")
#             .upsert(
#                 {
#                     "booking_id": booking["id"],
#                     "customer_name": booking.get(
#                         "customer_name"
#                     ),
#                     "staff_email": email,
#                     "service_type": booking.get(
#                         "service_type"
#                     ),
#                     "uploads": uploads,
#                     "updated_at": datetime.now(
#                         timezone.utc
#                     ).isoformat(),
#                 },
#                 on_conflict="booking_id",
#             )
#             .execute()
#         )

#         return {
#             "url": image_url,
#             "uploads": uploads,
#             "database": db_response.data,
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

#         if stage not in ("start", "end"):
#             raise ValueError(
#                 "Invalid photo stage."
#             )

#         field = (
#             "start_photo_url"
#             if stage == "start"
#             else "end_photo_url"
#         )

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     field: f"Skipped: {reason}",
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data















# from datetime import datetime, timezone

# from app.supabase.client import supabase


# class PartnerBookingRepository:

#     # =========================================================
#     # GET BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_bookings(
#         email: str,
#         status: str | None = None,
#     ):

#         query = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("assigned_staff_email", email)
#         )

#         # -----------------------------------------------------
#         # PENDING
#         # -----------------------------------------------------

#         if status == "pending":

#             query = (
#                 query
#                 .or_(
#                     "staff_response.is.null,staff_response.eq.pending"
#                 )
#                 .neq("work_status", "COMPLETED")
#                 .neq("work_status", "CANCELLED")
#             )

#         # -----------------------------------------------------
#         # ASSIGNED
#         # -----------------------------------------------------

#         elif status == "assigned":

#             query = (
#                 query
#                 .eq("staff_response", "APPROVED")
#                 .eq("work_status", "ASSIGNED")
#             )

#         # -----------------------------------------------------
#         # COMPLETED
#         # -----------------------------------------------------

#         elif status == "completed":

#             query = query.eq(
#                 "work_status",
#                 "COMPLETED",
#             )

#         # -----------------------------------------------------
#         # CANCELLED
#         # -----------------------------------------------------

#         elif status == "cancelled":

#             query = query.eq(
#                 "work_status",
#                 "CANCELLED",
#             )

#         # -----------------------------------------------------
#         # EXECUTE
#         # -----------------------------------------------------

#         response = (
#             query
#             .order(
#                 "booking_date",
#                 desc=True,
#             )
#             .execute()
#         )

#         return response.data or []

#     # =========================================================
#     # GET SINGLE BOOKING
#     # =========================================================

#     @staticmethod
#     def get_booking_for_partner(
#         booking_id: str,
#         email: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # GET BOOKING DETAILS
#     # =========================================================

#     @staticmethod
#     def get_booking_details(
#         booking_id: str,
#         email: str,
#     ):

#         # -----------------------------------------------------
#         # GET BOOKING
#         # -----------------------------------------------------

#         booking_response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         booking = (
#             booking_response.data
#             if booking_response is not None
#             else None
#         )

#         if not booking:
#             return None

#         # -----------------------------------------------------
#         # DEFAULT UPLOAD STRUCTURE
#         # -----------------------------------------------------

#         uploads = {
#             "before": {},
#             "after": {},
#         }

#         # -----------------------------------------------------
#         # GET SERVICE UPLOADS
#         # -----------------------------------------------------

#         try:

#             uploads_response = (
#                 supabase
#                 .table("service_uploads")
#                 .select("uploads")
#                 .eq(
#                     "booking_id",
#                     booking_id,
#                 )
#                 .maybe_single()
#                 .execute()
#             )

#             if uploads_response is not None:

#                 uploads_data = (
#                     uploads_response.data
#                     or {}
#                 )

#                 if isinstance(
#                     uploads_data,
#                     dict,
#                 ):

#                     stored_uploads = (
#                         uploads_data.get(
#                             "uploads"
#                         )
#                     )

#                     if isinstance(
#                         stored_uploads,
#                         dict,
#                     ):

#                         uploads = stored_uploads

#         except Exception as error:

#             # A booking can exist before a
#             # service_uploads row is created.
#             #
#             # Do not fail booking details just
#             # because uploads do not exist yet.

#             print(
#                 "SERVICE UPLOADS FETCH ERROR:",
#                 repr(error),
#             )

#         # -----------------------------------------------------
#         # MAKE SURE BEFORE / AFTER EXIST
#         # -----------------------------------------------------

#         if not isinstance(
#             uploads.get("before"),
#             dict,
#         ):
#             uploads["before"] = {}

#         if not isinstance(
#             uploads.get("after"),
#             dict,
#         ):
#             uploads["after"] = {}

#         # -----------------------------------------------------
#         # GET SERVICE DETAILS
#         # -----------------------------------------------------

#         service_id = None

#         services = booking.get(
#             "services"
#         )

#         if (
#             isinstance(services, list)
#             and services
#         ):

#             first_service = services[0]

#             if isinstance(
#                 first_service,
#                 dict,
#             ):
#                 service_id = first_service.get(
#                     "id"
#                 )

#             else:
#                 service_id = first_service

#         service = None

#         # -----------------------------------------------------
#         # GET SERVICE
#         # -----------------------------------------------------

#         if service_id:

#             try:

#                 service_response = (
#                     supabase
#                     .table("services")
#                     .select(
#                         "id, staff_amount, service_type"
#                     )
#                     .eq(
#                         "id",
#                         service_id,
#                     )
#                     .maybe_single()
#                     .execute()
#                 )

#                 if service_response is not None:
#                     service = (
#                         service_response.data
#                     )

#             except Exception as error:

#                 print(
#                     "SERVICE DETAILS FETCH ERROR:",
#                     repr(error),
#                 )

#         # -----------------------------------------------------
#         # FINAL RESPONSE
#         # -----------------------------------------------------

#         return {
#             "booking": booking,

#             "uploads": uploads,

#             "service": (
#                 service
#                 if isinstance(
#                     service,
#                     dict,
#                 )
#                 else {}
#             ),
#         }

#     # =========================================================
#     # GET SERVICE UPLOADS
#     # =========================================================

#     @staticmethod
#     def get_service_uploads(
#         booking_id: str,
#     ):

#         response = (
#             supabase
#             .table("service_uploads")
#             .select("uploads")
#             .eq("booking_id", booking_id)
#             .maybe_single()
#             .execute()
#         )

#         if response is None or not response.data:
#             return {
#                 "before": {},
#                 "after": {},
#             }

#         uploads = response.data.get("uploads")

#         return uploads or {
#             "before": {},
#             "after": {},
#         }

#     # =========================================================
#     # APPROVE BOOKING
#     # =========================================================

#     @staticmethod
#     def approve_booking(
#         booking_id: str,
#         email: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "staff_response": "APPROVED",
#                     "work_status": "ASSIGNED",
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # REJECT BOOKING
#     # =========================================================

#     @staticmethod
#     def reject_booking(
#         booking_id: str,
#         email: str,
#         reason: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "staff_response": "REJECTED",
#                     "reject_reason": reason,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # CANCEL ASSIGNED BOOKING
#     # =========================================================

#     @staticmethod
#     def cancel_booking(
#         booking_id: str,
#         email: str,
#         reason: str,
#         cancellation_fee: float = 99,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "work_status": "CANCELLED",
#                     "cancel_reason": reason,
#                     "cancel_requested": True,
#                     "cancellation_fee": cancellation_fee,
#                     "cancel_time": datetime.now(
#                         timezone.utc
#                     ).isoformat(),
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .eq("staff_response", "APPROVED")
#             .eq("work_status", "ASSIGNED")
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # START WORK
#     # =========================================================

#     @staticmethod
#     def start_work(
#         booking_id: str,
#         email: str,
#         start_time: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "work_started_at": start_time,
#                     "work_status": "ASSIGNED",
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .eq("staff_response", "APPROVED")
#             .eq("work_status", "ASSIGNED")
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # COMPLETE WORK
#     # =========================================================

#     @staticmethod
#     def complete_work(
#         booking_id: str,
#         email: str,
#         worked_duration: str,
#         staff_amount: float,
#         end_time: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "work_status": "COMPLETED",
#                     "worked_duration": worked_duration,
#                     "staff_earned_amount": staff_amount,
#                     "work_ended_at": end_time,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .eq("staff_response", "APPROVED")
#             .eq("work_status", "ASSIGNED")
#             .not_.is_(
#                 "work_started_at",
#                 "null",
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # INSERT STAFF EARNINGS
#     # =========================================================

#     @staticmethod
#     def insert_staff_earning(
#         booking: dict,
#         amount: float,
#     ):

#         response = (
#             supabase
#             .table("staff_earnings")
#             .insert(
#                 {
#                     "booking_id": booking["id"],
#                     "staff_email": booking[
#                         "assigned_staff_email"
#                     ],
#                     "Customer_Name": booking[
#                         "customer_name"
#                     ],
#                     "AMOUNT": amount,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # UPDATE COMPLETED COUNT
#     # =========================================================

#     @staticmethod
#     def update_completed_count(
#         email: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .select(
#                 "id",
#                 count="exact",
#                 head=True,
#             )
#             .eq(
#                 "assigned_staff_email",
#                 email,
#             )
#             .eq(
#                 "work_status",
#                 "COMPLETED",
#             )
#             .execute()
#         )

#         completed_count = response.count or 0

#         profile_response = (
#             supabase
#             .table("staff_profile")
#             .update(
#                 {
#                     "total_completed": completed_count,
#                 }
#             )
#             .eq("email", email)
#             .execute()
#         )

#         return profile_response.data


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
#         # VALIDATE STAGE
#         # -----------------------------------------------------

#         if stage not in (
#             "before",
#             "after",
#         ):
#             raise ValueError(
#                 "Invalid photo stage."
#             )

#         # -----------------------------------------------------
#         # VALIDATE REASON
#         # -----------------------------------------------------

#         if not reason or not reason.strip():
#             raise ValueError(
#                 "Skip reason is required."
#             )

#         # -----------------------------------------------------
#         # GET BOOKING
#         # -----------------------------------------------------

#         booking_response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("assigned_staff_email", email)
#             .maybe_single()
#             .execute()
#         )

#         if (
#             booking_response is None
#             or not booking_response.data
#         ):
#             return None

#         booking = booking_response.data

#         # -----------------------------------------------------
#         # CHECK BOOKING STATUS
#         # -----------------------------------------------------

#         work_status = str(
#             booking.get("work_status") or ""
#         ).strip().upper()

#         if work_status in (
#             "COMPLETED",
#             "CANCELLED",
#         ):
#             raise ValueError(
#                 "This booking is no longer active."
#             )

#         # -----------------------------------------------------
#         # GET EXISTING UPLOADS
#         # -----------------------------------------------------

#         uploads = {
#             "before": {},
#             "after": {},
#         }

#         try:

#             uploads_response = (
#                 supabase
#                 .table("service_uploads")
#                 .select("uploads")
#                 .eq(
#                     "booking_id",
#                     booking_id,
#                 )
#                 .maybe_single()
#                 .execute()
#             )

#             if uploads_response is not None:

#                 data = (
#                     uploads_response.data
#                     or {}
#                 )

#                 if isinstance(data, dict):

#                     existing_uploads = (
#                         data.get("uploads")
#                     )

#                     if isinstance(
#                         existing_uploads,
#                         dict,
#                     ):
#                         uploads = existing_uploads

#         except Exception as error:

#             print(
#                 "SKIP PHOTO FETCH ERROR:",
#                 repr(error),
#             )

#         # -----------------------------------------------------
#         # MAKE SURE BEFORE / AFTER EXIST
#         # -----------------------------------------------------

#         if not isinstance(
#             uploads.get("before"),
#             dict,
#         ):
#             uploads["before"] = {}

#         if not isinstance(
#             uploads.get("after"),
#             dict,
#         ):
#             uploads["after"] = {}

#         # -----------------------------------------------------
#         # SAVE SKIP INFORMATION
#         # -----------------------------------------------------

#         uploads[stage]["_skipped"] = True

#         uploads[stage]["_skip_reason"] = (
#             reason.strip()
#         )

#         # -----------------------------------------------------
#         # UPSERT SERVICE UPLOADS
#         # -----------------------------------------------------

#         response = (
#             supabase
#             .table("service_uploads")
#             .upsert(
#                 {
#                     "booking_id": booking_id,
#                     "customer_name": booking.get(
#                         "customer_name"
#                     ),
#                     "staff_email": email,
#                     "service_type": booking.get(
#                         "service_type"
#                     ),
#                     "uploads": uploads,
#                     "updated_at": datetime.now(
#                         timezone.utc
#                     ).isoformat(),
#                 },
#                 on_conflict="booking_id",
#             )
#             .execute()
#         )

#         # -----------------------------------------------------
#         # RETURN
#         # -----------------------------------------------------

#         return response.data

#     # =========================================================
#     # SAVE PHOTO
#     # =========================================================

#     @staticmethod
#     def save_photo(
#         booking: dict,
#         email: str,
#         stage: str,
#         category: str,
#         file_bytes: bytes,
#         content_type: str = "image/jpeg",
#     ):

#         # -----------------------------------------------------
#         # VALIDATE STAGE
#         # -----------------------------------------------------

#         if stage not in (
#             "before",
#             "after",
#         ):
#             raise ValueError(
#                 "Invalid photo stage."
#             )

#         if not file_bytes:
#             raise ValueError(
#                 "Uploaded file is empty."
#             )

#         # -----------------------------------------------------
#         # BUILD STORAGE PATH
#         # -----------------------------------------------------

#         safe_customer_name = (
#             booking.get(
#                 "customer_name",
#                 "customer",
#             )
#             .replace(" ", "_")
#         )

#         folder_name = (
#             f"{safe_customer_name}_({booking['id']})"
#         )

#         file_path = (
#             f"{email}/"
#             f"{folder_name}/"
#             f"{stage}/"
#             f"{category}.jpg"
#         )

#         # -----------------------------------------------------
#         # UPLOAD TO SUPABASE STORAGE
#         # -----------------------------------------------------

#         try:

#             supabase.storage \
#                 .from_("work_uploads") \
#                 .upload(
#                     file_path,
#                     file_bytes,
#                     {
#                         "content-type": content_type,
#                         "upsert": "true",
#                     },
#                 )

#         except Exception as error:

#             print(
#                 "STORAGE UPLOAD ERROR:",
#                 repr(error),
#             )

#             raise

#         # -----------------------------------------------------
#         # GET PUBLIC URL
#         # -----------------------------------------------------

#         try:

#             public_data = (
#                 supabase.storage
#                 .from_("work_uploads")
#                 .get_public_url(
#                     file_path
#                 )
#             )

#             image_url = public_data

#             if isinstance(
#                 public_data,
#                 dict,
#             ):
#                 image_url = (
#                     public_data.get("publicUrl")
#                     or public_data.get("public_url")
#                 )

#             if not image_url:
#                 raise ValueError(
#                     "Unable to generate public image URL."
#                 )

#         except Exception as error:

#             print(
#                 "PUBLIC URL ERROR:",
#                 repr(error),
#             )

#             raise

#         # -----------------------------------------------------
#         # GET EXISTING UPLOADS
#         # -----------------------------------------------------

#         uploads = None

#         try:

#             existing_response = (
#                 supabase
#                 .table("service_uploads")
#                 .select("uploads")
#                 .eq(
#                     "booking_id",
#                     booking["id"],
#                 )
#                 .maybe_single()
#                 .execute()
#             )

#             if existing_response is not None:

#                 response_data = (
#                     existing_response.data
#                     or {}
#                 )

#                 if isinstance(
#                     response_data,
#                     dict,
#                 ):
#                     uploads = (
#                         response_data.get(
#                             "uploads"
#                         )
#                     )

#         except Exception as error:

#             print(
#                 "EXISTING UPLOADS FETCH ERROR:",
#                 repr(error),
#             )

#             # No existing upload record is okay.
#             uploads = None

#         # -----------------------------------------------------
#         # DEFAULT UPLOAD STRUCTURE
#         # -----------------------------------------------------

#         if not isinstance(
#             uploads,
#             dict,
#         ):
#             uploads = {
#                 "before": {},
#                 "after": {},
#             }

#         if not isinstance(
#             uploads.get("before"),
#             dict,
#         ):
#             uploads["before"] = {}

#         if not isinstance(
#             uploads.get("after"),
#             dict,
#         ):
#             uploads["after"] = {}

#         # -----------------------------------------------------
#         # ADD NEW PHOTO
#         # -----------------------------------------------------

#         uploads[stage][category] = image_url

#         # -----------------------------------------------------
#         # UPSERT SERVICE UPLOADS
#         # -----------------------------------------------------

#         db_response = (
#             supabase
#             .table("service_uploads")
#             .upsert(
#                 {
#                     "booking_id": booking["id"],
#                     "customer_name": booking.get(
#                         "customer_name"
#                     ),
#                     "staff_email": email,
#                     "service_type": booking.get(
#                         "service_type"
#                     ),
#                     "uploads": uploads,
#                     "updated_at": datetime.now(
#                         timezone.utc
#                     ).isoformat(),
#                 },
#                 on_conflict="booking_id",
#             )
#             .execute()
#         )

#         # -----------------------------------------------------
#         # RESPONSE
#         # -----------------------------------------------------

#         return {
#             "url": image_url,
#             "uploads": uploads,
#             "database": (
#                 db_response.data
#                 if db_response is not None
#                 else None
#             ),
#         }








from datetime import datetime, timezone

from app.supabase.client import supabase


class PartnerBookingRepository:

    # =========================================================
    # GET BOOKINGS
    # =========================================================

    @staticmethod
    def get_bookings(
        email: str,
        status: str | None = None,
    ):

        query = (
            supabase
            .table("bookings")
            .select("*")
            .eq("assigned_staff_email", email)
        )

        # -----------------------------------------------------
        # PENDING
        # -----------------------------------------------------

        if status == "pending":

            query = (
                query
                .or_(
                    "staff_response.is.null,staff_response.eq.pending"
                )
                .neq("work_status", "COMPLETED")
                .neq("work_status", "CANCELLED")
            )

        # -----------------------------------------------------
        # ASSIGNED
        # -----------------------------------------------------

        # elif status == "assigned":

        #     query = (
        #         query
        #         .eq("staff_response", "APPROVED")
        #         .eq("work_status", "ASSIGNED")
        #     )
        elif status == "assigned":
            query = (
                query
                # .or_("staff_response.is.null,staff_response.eq.APPROVED")
                .eq("work_status", "ASSIGNED")
            )

        # -----------------------------------------------------
        # COMPLETED
        # -----------------------------------------------------

        elif status == "completed":

            query = query.eq(
                "work_status",
                "COMPLETED",
            )

        # -----------------------------------------------------
        # CANCELLED
        # -----------------------------------------------------

        elif status == "cancelled":

            query = query.eq(
                "work_status",
                "CANCELLED",
            )

        # -----------------------------------------------------
        # EXECUTE
        # -----------------------------------------------------

        response = (
            query
            .order(
                "booking_date",
                desc=True,
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # GET SINGLE BOOKING
    # =========================================================

    @staticmethod
    def get_booking_for_partner(
        booking_id: str,
        email: str,
    ):

        response = (
            supabase
            .table("bookings")
            .select("*")
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # GET BOOKING DETAILS
    # =========================================================

    @staticmethod
    def get_booking_details(
        booking_id: str,
        email: str,
    ):

        # -----------------------------------------------------
        # GET BOOKING
        # -----------------------------------------------------

        booking_response = (
            supabase
            .table("bookings")
            .select("*")
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            .maybe_single()
            .execute()
        )

        booking = (
            booking_response.data
            if booking_response is not None
            else None
        )

        if not booking:
            return None

        # -----------------------------------------------------
        # DEFAULT UPLOAD STRUCTURE
        # -----------------------------------------------------

        uploads = {
            "before": {},
            "after": {},
        }

        # -----------------------------------------------------
        # GET SERVICE UPLOADS
        # -----------------------------------------------------

        try:

            uploads_response = (
                supabase
                .table("service_uploads")
                .select("uploads")
                .eq(
                    "booking_id",
                    booking_id,
                )
                .maybe_single()
                .execute()
            )

            if uploads_response is not None:

                uploads_data = (
                    uploads_response.data
                    or {}
                )

                if isinstance(
                    uploads_data,
                    dict,
                ):

                    stored_uploads = (
                        uploads_data.get(
                            "uploads"
                        )
                    )

                    if isinstance(
                        stored_uploads,
                        dict,
                    ):

                        uploads = stored_uploads

        except Exception as error:

            # A booking can exist before a
            # service_uploads row is created.
            #
            # Do not fail booking details just
            # because uploads do not exist yet.

            print(
                "SERVICE UPLOADS FETCH ERROR:",
                repr(error),
            )

        # -----------------------------------------------------
        # MAKE SURE BEFORE / AFTER EXIST
        # -----------------------------------------------------

        if not isinstance(
            uploads.get("before"),
            dict,
        ):
            uploads["before"] = {}

        if not isinstance(
            uploads.get("after"),
            dict,
        ):
            uploads["after"] = {}

        # -----------------------------------------------------
        # GET SERVICE DETAILS
        # -----------------------------------------------------

        service_id = None

        services = booking.get(
            "services"
        )

        if (
            isinstance(services, list)
            and services
        ):

            first_service = services[0]

            if isinstance(
                first_service,
                dict,
            ):
                service_id = first_service.get(
                    "id"
                )

            else:
                service_id = first_service

        service = None

        # -----------------------------------------------------
        # GET SERVICE
        # -----------------------------------------------------

        if service_id:

            try:

                service_response = (
                    supabase
                    .table("services")
                    .select(
                        "id, staff_amount, service_type"
                    )
                    .eq(
                        "id",
                        service_id,
                    )
                    .maybe_single()
                    .execute()
                )

                if service_response is not None:
                    service = (
                        service_response.data
                    )

            except Exception as error:

                print(
                    "SERVICE DETAILS FETCH ERROR:",
                    repr(error),
                )

        # -----------------------------------------------------
        # FINAL RESPONSE
        # -----------------------------------------------------

        return {
            "booking": booking,

            "uploads": uploads,

            "service": (
                service
                if isinstance(
                    service,
                    dict,
                )
                else {}
            ),
        }

    # =========================================================
    # GET SERVICE UPLOADS
    # =========================================================

    @staticmethod
    def get_service_uploads(
        booking_id: str,
    ):

        response = (
            supabase
            .table("service_uploads")
            .select("uploads")
            .eq("booking_id", booking_id)
            .maybe_single()
            .execute()
        )

        if response is None or not response.data:
            return {
                "before": {},
                "after": {},
            }

        uploads = response.data.get("uploads")

        return uploads or {
            "before": {},
            "after": {},
        }

    # =========================================================
    # APPROVE BOOKING
    # =========================================================

    @staticmethod
    def approve_booking(
        booking_id: str,
        email: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "staff_response": "APPROVED",
                    "work_status": "ASSIGNED",
                }
            )
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            .execute()
        )

        return response.data

    # =========================================================
    # REJECT BOOKING
    # =========================================================

    @staticmethod
    def reject_booking(
        booking_id: str,
        email: str,
        reason: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "staff_response": "REJECTED",
                    "reject_reason": reason,
                }
            )
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            .execute()
        )

        return response.data

    # =========================================================
    # CANCEL ASSIGNED BOOKING
    # =========================================================

    @staticmethod
    def cancel_booking(
        booking_id: str,
        email: str,
        reason: str,
        cancellation_fee: float = 99,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "work_status": "CANCELLED",
                    "cancel_reason": reason,
                    "cancel_requested": True,
                    "cancellation_fee": cancellation_fee,
                    "cancel_time": datetime.now(
                        timezone.utc
                    ).isoformat(),
                }
            )
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            # .eq("staff_response", "APPROVED")
            .eq("work_status", "ASSIGNED")
            .execute()
        )

        return response.data

    # =========================================================
    # START WORK
    # =========================================================

    @staticmethod
    def start_work(
        booking_id: str,
        email: str,
        start_time: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "work_started_at": start_time,
                    "work_status": "ASSIGNED",
                }
            )
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            # .eq("staff_response", "APPROVED")
            .eq("work_status", "ASSIGNED")
            .execute()
        )

        return response.data

    # =========================================================
    # COMPLETE WORK
    # =========================================================

    @staticmethod
    def complete_work(
        booking_id: str,
        email: str,
        worked_duration: str,
        staff_amount: float,
        end_time: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "work_status": "COMPLETED",
                    "worked_duration": worked_duration,
                    "staff_earned_amount": staff_amount,
                    "work_ended_at": end_time,
                }
            )
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            # .eq("staff_response", "APPROVED")
            .eq("work_status", "ASSIGNED")
            .not_.is_(
                "work_started_at",
                "null",
            )
            .execute()
        )

        return response.data

    # =========================================================
    # INSERT STAFF EARNINGS
    # =========================================================

    @staticmethod
    def insert_staff_earning(
        booking: dict,
        amount: float,
    ):

        response = (
            supabase
            .table("staff_earnings")
            .insert(
                {
                    "booking_id": booking["id"],
                    "staff_email": booking[
                        "assigned_staff_email"
                    ],
                    "Customer_Name": booking[
                        "customer_name"
                    ],
                    "AMOUNT": amount,
                }
            )
            .execute()
        )

        return response.data

    # =========================================================
    # UPDATE COMPLETED COUNT
    # =========================================================

    @staticmethod
    def update_completed_count(
        email: str,
    ):

        response = (
            supabase
            .table("bookings")
            .select(
                "id",
                count="exact",
                head=True,
            )
            .eq(
                "assigned_staff_email",
                email,
            )
            .eq(
                "work_status",
                "COMPLETED",
            )
            .execute()
        )

        completed_count = response.count or 0

        profile_response = (
            supabase
            .table("staff_profile")
            .update(
                {
                    "total_completed": completed_count,
                }
            )
            .eq("email", email)
            .execute()
        )

        return profile_response.data


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
        # VALIDATE STAGE
        # -----------------------------------------------------

        if stage not in (
            "before",
            "after",
        ):
            raise ValueError(
                "Invalid photo stage."
            )

        # -----------------------------------------------------
        # VALIDATE REASON
        # -----------------------------------------------------

        if not reason or not reason.strip():
            raise ValueError(
                "Skip reason is required."
            )

        # -----------------------------------------------------
        # GET BOOKING
        # -----------------------------------------------------

        booking_response = (
            supabase
            .table("bookings")
            .select("*")
            .eq("id", booking_id)
            .eq("assigned_staff_email", email)
            .maybe_single()
            .execute()
        )

        if (
            booking_response is None
            or not booking_response.data
        ):
            return None

        booking = booking_response.data

        # -----------------------------------------------------
        # CHECK BOOKING STATUS
        # -----------------------------------------------------

        work_status = str(
            booking.get("work_status") or ""
        ).strip().upper()

        if work_status in (
            "COMPLETED",
            "CANCELLED",
        ):
            raise ValueError(
                "This booking is no longer active."
            )

        # -----------------------------------------------------
        # GET EXISTING UPLOADS
        # -----------------------------------------------------

        uploads = {
            "before": {},
            "after": {},
        }

        try:

            uploads_response = (
                supabase
                .table("service_uploads")
                .select("uploads")
                .eq(
                    "booking_id",
                    booking_id,
                )
                .maybe_single()
                .execute()
            )

            if uploads_response is not None:

                data = (
                    uploads_response.data
                    or {}
                )

                if isinstance(data, dict):

                    existing_uploads = (
                        data.get("uploads")
                    )

                    if isinstance(
                        existing_uploads,
                        dict,
                    ):
                        uploads = existing_uploads

        except Exception as error:

            print(
                "SKIP PHOTO FETCH ERROR:",
                repr(error),
            )

        # -----------------------------------------------------
        # MAKE SURE BEFORE / AFTER EXIST
        # -----------------------------------------------------

        if not isinstance(
            uploads.get("before"),
            dict,
        ):
            uploads["before"] = {}

        if not isinstance(
            uploads.get("after"),
            dict,
        ):
            uploads["after"] = {}

        # -----------------------------------------------------
        # SAVE SKIP INFORMATION
        # -----------------------------------------------------

        uploads[stage]["_skipped"] = True

        uploads[stage]["_skip_reason"] = (
            reason.strip()
        )

        # -----------------------------------------------------
        # UPSERT SERVICE UPLOADS
        # -----------------------------------------------------

        response = (
            supabase
            .table("service_uploads")
            .upsert(
                {
                    "booking_id": booking_id,
                    "customer_name": booking.get(
                        "customer_name"
                    ),
                    "staff_email": email,
                    "service_type": booking.get(
                        "service_type"
                    ),
                    "uploads": uploads,
                    "updated_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                },
                on_conflict="booking_id",
            )
            .execute()
        )

        # -----------------------------------------------------
        # RETURN
        # -----------------------------------------------------

        return response.data

    # =========================================================
    # SAVE PHOTO
    # =========================================================

    @staticmethod
    def save_photo(
        booking: dict,
        email: str,
        stage: str,
        category: str,
        file_bytes: bytes,
        content_type: str = "image/jpeg",
    ):

        # -----------------------------------------------------
        # VALIDATE STAGE
        # -----------------------------------------------------

        if stage not in (
            "before",
            "after",
        ):
            raise ValueError(
                "Invalid photo stage."
            )

        if not file_bytes:
            raise ValueError(
                "Uploaded file is empty."
            )

        # -----------------------------------------------------
        # BUILD STORAGE PATH
        # -----------------------------------------------------

        safe_customer_name = (
            booking.get(
                "customer_name",
                "customer",
            )
            .replace(" ", "_")
        )

        folder_name = (
            f"{safe_customer_name}_({booking['id']})"
        )

        file_path = (
            f"{email}/"
            f"{folder_name}/"
            f"{stage}/"
            f"{category}.jpg"
        )

        # -----------------------------------------------------
        # UPLOAD TO SUPABASE STORAGE
        # -----------------------------------------------------

        try:

            supabase.storage \
                .from_("work_uploads") \
                .upload(
                    file_path,
                    file_bytes,
                    {
                        "content-type": content_type,
                        "upsert": "true",
                    },
                )

        except Exception as error:

            print(
                "STORAGE UPLOAD ERROR:",
                repr(error),
            )

            raise

        # -----------------------------------------------------
        # GET PUBLIC URL
        # -----------------------------------------------------

        try:

            public_data = (
                supabase.storage
                .from_("work_uploads")
                .get_public_url(
                    file_path
                )
            )

            image_url = public_data

            if isinstance(
                public_data,
                dict,
            ):
                image_url = (
                    public_data.get("publicUrl")
                    or public_data.get("public_url")
                )

            if not image_url:
                raise ValueError(
                    "Unable to generate public image URL."
                )

        except Exception as error:

            print(
                "PUBLIC URL ERROR:",
                repr(error),
            )

            raise

        # -----------------------------------------------------
        # GET EXISTING UPLOADS
        # -----------------------------------------------------

        uploads = None

        try:

            existing_response = (
                supabase
                .table("service_uploads")
                .select("uploads")
                .eq(
                    "booking_id",
                    booking["id"],
                )
                .maybe_single()
                .execute()
            )

            if existing_response is not None:

                response_data = (
                    existing_response.data
                    or {}
                )

                if isinstance(
                    response_data,
                    dict,
                ):
                    uploads = (
                        response_data.get(
                            "uploads"
                        )
                    )

        except Exception as error:

            print(
                "EXISTING UPLOADS FETCH ERROR:",
                repr(error),
            )

            # No existing upload record is okay.
            uploads = None

        # -----------------------------------------------------
        # DEFAULT UPLOAD STRUCTURE
        # -----------------------------------------------------

        if not isinstance(
            uploads,
            dict,
        ):
            uploads = {
                "before": {},
                "after": {},
            }

        if not isinstance(
            uploads.get("before"),
            dict,
        ):
            uploads["before"] = {}

        if not isinstance(
            uploads.get("after"),
            dict,
        ):
            uploads["after"] = {}

        # -----------------------------------------------------
        # ADD NEW PHOTO
        # -----------------------------------------------------

        uploads[stage][category] = image_url

        # -----------------------------------------------------
        # UPSERT SERVICE UPLOADS
        # -----------------------------------------------------

        db_response = (
            supabase
            .table("service_uploads")
            .upsert(
                {
                    "booking_id": booking["id"],
                    "customer_name": booking.get(
                        "customer_name"
                    ),
                    "staff_email": email,
                    "service_type": booking.get(
                        "service_type"
                    ),
                    "uploads": uploads,
                    "updated_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                },
                on_conflict="booking_id",
            )
            .execute()
        )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        return {
            "url": image_url,
            "uploads": uploads,
            "database": (
                db_response.data
                if db_response is not None
                else None
            ),
        }