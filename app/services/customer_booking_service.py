# from datetime import date

# from fastapi import HTTPException, status

# from app.repositories.customer_booking_repository import (
#     CustomerBookingRepository,
# )

# from app.repositories.customer_booking_repository import (
#     CustomerBookingRepository,
# )


# class CustomerBookingService:

#     # =========================================================
#     # PRICE HELPER
#     # =========================================================

#     @staticmethod
#     def _parse_price(value) -> float:

#         if value is None:
#             return 0.0

#         try:
#             return float(
#                 str(value)
#                 .replace("₹", "")
#                 .replace(",", "")
#                 .strip()
#             )

#         except (ValueError, TypeError):
#             return 0.0

#     # =========================================================
#     # QUANTITY HELPER
#     # =========================================================

#     @staticmethod
#     def _get_quantity(item: dict) -> int:

#         quantity = item.get(
#             "quantity",
#             1,
#         )

#         try:
#             quantity = int(quantity)

#         except (ValueError, TypeError):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid item quantity.",
#             )

#         if quantity <= 0:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Quantity must be greater than zero.",
#             )

#         return quantity

#     # =========================================================
#     # CREATE BOOKING
#     # =========================================================

#     @staticmethod
#     def create_booking(
#         user_id: str,
#         customer_name: str,
#         email: str,
#         phone_number: str,
#         full_address: str,
#         services,
#         booking_date,
#         booking_time: str,
#         add_ons=None,
#         latitude=None,
#         longitude=None,
#         location_link=None,
#     ):

#         # =====================================================
#         # BASIC VALIDATION
#         # =====================================================

#         customer_name = customer_name.strip()
#         email = email.strip()
#         phone_number = phone_number.strip()
#         full_address = full_address.strip()
#         booking_time = booking_time.strip()

#         if not customer_name:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Customer name is required.",
#             )

#         if not email:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Email is required.",
#             )

#         if not phone_number:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Phone number is required.",
#             )

#         if not full_address:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Address is required.",
#             )

#         if not booking_time:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Booking time is required.",
#             )

#         # =====================================================
#         # DATE VALIDATION
#         # =====================================================

#         if isinstance(booking_date, str):

#             try:
#                 booking_date = date.fromisoformat(
#                     booking_date
#                 )

#             except ValueError:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Invalid booking date. "
#                         "Use YYYY-MM-DD."
#                     ),
#                 )

#         if not isinstance(booking_date, date):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid booking date.",
#             )

#         if booking_date < date.today():
#             raise HTTPException(
#                 status_code=400,
#                 detail="Booking date cannot be in the past.",
#             )

#         # =====================================================
#         # SERVICES VALIDATION
#         # =====================================================

#         if not services:
#             raise HTTPException(
#                 status_code=400,
#                 detail="At least one service is required.",
#             )

#         service_ids = []

#         for item in services:

#             if not isinstance(item, dict):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each service must be an object."
#                     ),
#                 )

#             service_id = item.get("id")

#             if not service_id:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each service must contain an id."
#                     ),
#                 )

#             service_ids.append(
#                 str(service_id)
#             )

#         # Prevent duplicate services.
#         if len(service_ids) != len(set(service_ids)):
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Duplicate services are not allowed."
#                 ),
#             )

#         # =====================================================
#         # GET SERVICES FROM DATABASE
#         # =====================================================

#         db_services = (
#             CustomerBookingRepository
#             .get_services_by_ids(
#                 service_ids
#             )
#         )

#         if len(db_services) != len(service_ids):
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "One or more selected services "
#                     "are invalid."
#                 ),
#             )

#         service_map = {
#             str(service["id"]): service
#             for service in db_services
#         }

#         # =====================================================
#         # ADD-ONS VALIDATION
#         # =====================================================

#         add_ons = add_ons or []

#         addon_ids = []

#         for item in add_ons:

#             if not isinstance(item, dict):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each add-on must be an object."
#                     ),
#                 )

#             addon_id = item.get("id")

#             if not addon_id:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each add-on must contain an id."
#                     ),
#                 )

#             addon_ids.append(
#                 str(addon_id)
#             )

#         # Prevent duplicate add-ons.
#         if len(addon_ids) != len(set(addon_ids)):
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Duplicate add-ons are not allowed."
#                 ),
#             )

#         db_addons = []

#         if addon_ids:

#             db_addons = (
#                 CustomerBookingRepository
#                 .get_addons_by_ids(
#                     addon_ids
#                 )
#             )

#             if len(db_addons) != len(addon_ids):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "One or more selected add-ons "
#                         "are invalid."
#                     ),
#                 )

#         addon_map = {
#             str(addon["id"]): addon
#             for addon in db_addons
#         }

#         # =====================================================
#         # CALCULATE TOTAL
#         # =====================================================

#         calculated_total = 0.0

#         normalized_services = []

#         # =====================================================
#         # SERVICES
#         # =====================================================

#         for item in services:

#             service_id = str(
#                 item["id"]
#             )

#             quantity = (
#                 CustomerBookingService
#                 ._get_quantity(item)
#             )

#             service = service_map[
#                 service_id
#             ]

#             price = (
#                 CustomerBookingService
#                 ._parse_price(
#                     service.get("price")
#                 )
#             )

#             if price <= 0:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         f"Invalid service price for "
#                         f"'{service.get('title')}'."
#                     ),
#                 )

#             line_total = (
#                 price * quantity
#             )

#             calculated_total += line_total

#             normalized_services.append(
#                 {
#                     "id": service_id,
#                     "title": service.get(
#                         "title"
#                     ),
#                     "quantity": quantity,
#                     "price": price,
#                 }
#             )

#         # =====================================================
#         # ADD-ONS
#         # =====================================================

#         normalized_addons = []

#         for item in add_ons:

#             addon_id = str(
#                 item["id"]
#             )

#             quantity = (
#                 CustomerBookingService
#                 ._get_quantity(item)
#             )

#             addon = addon_map[
#                 addon_id
#             ]

#             price = (
#                 CustomerBookingService
#                 ._parse_price(
#                     addon.get("price")
#                 )
#             )

#             if price <= 0:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         f"Invalid add-on price for "
#                         f"'{addon.get('title')}'."
#                     ),
#                 )

#             line_total = (
#                 price * quantity
#             )

#             calculated_total += line_total

#             normalized_addons.append(
#                 {
#                     "id": addon_id,
#                     "title": addon.get(
#                         "title"
#                     ),
#                     "quantity": quantity,
#                     "price": price,
#                 }
#             )

#         # =====================================================
#         # FINAL TOTAL
#         # =====================================================

#         calculated_total = round(
#             calculated_total,
#             2,
#         )

#         if calculated_total <= 0:
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Booking amount must be "
#                     "greater than zero."
#                 ),
#             )

#         # =====================================================
#         # CREATE BOOKING
#         # =====================================================

#         booking = (
#             CustomerBookingRepository
#             .create_booking(
#                 customer_name=customer_name,
#                 email=email,
#                 phone_number=phone_number,
#                 full_address=full_address,

#                 services=normalized_services,

#                 add_ons=normalized_addons,

#                 booking_date=booking_date.isoformat(),

#                 booking_time=booking_time,

#                 total_amount=calculated_total,

#                 user_id=user_id,

#                 latitude=latitude,

#                 longitude=longitude,

#                 location_link=location_link,
#             )
#         )

#         # =====================================================
#         # INSERT FAILURE
#         # =====================================================

#         if not booking:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Failed to create booking.",
#             )

#         # =====================================================
#         # RESPONSE
#         # =====================================================

#         return {
#             "success": True,

#             "booking_id": str(
#                 booking["id"]
#             ),

#             "message": (
#                 "Booking created successfully."
#             ),

#             "payment_status": booking.get(
#                 "payment_status",
#                 "pending",
#             ),

#             "payment_verified": bool(
#                 booking.get(
#                     "payment_verified",
#                     False,
#                 )
#             ),

#             "total_amount": float(
#                 booking.get(
#                     "total_amount",
#                     calculated_total,
#                 )
#             ),
#         }
#         # =========================================================
#     # GET CUSTOMER BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_customer_bookings(
#         user_id: str,
#     ):
#         return CustomerBookingRepository.get_customer_bookings(
#             user_id=user_id
#         )



















# from fastapi import HTTPException, status

# from app.repositories.customer_booking_repository import (
#     CustomerBookingRepository,
# )


# class CustomerBookingService:

#     # =========================================================
#     # CREATE BOOKING
#     # =========================================================

#     @staticmethod
#     def create_booking(
#         user_id: str,
#         customer_name: str,
#         email: str,
#         phone_number: str,
#         full_address: str,
#         services,
#         add_ons,
#         booking_date,
#         booking_time: str,
#         latitude: float | None = None,
#         longitude: float | None = None,
#         location_link: str | None = None,
#     ):

#         # =====================================================
#         # BASIC VALIDATION
#         # =====================================================

#         customer_name = (
#             customer_name.strip()
#         )

#         email = email.strip()

#         phone_number = (
#             phone_number.strip()
#         )

#         full_address = (
#             full_address.strip()
#         )

#         booking_time = (
#             booking_time.strip()
#         )

#         if not customer_name:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Customer name is required.",
#             )

#         if not email:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Email is required.",
#             )

#         if not phone_number:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Phone number is required.",
#             )

#         if not full_address:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Address is required.",
#             )

#         if not services:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="At least one service is required.",
#             )

#         # =====================================================
#         # VALIDATE SERVICE IDS
#         # =====================================================

#         service_ids = []

#         for item in services:

#             if not isinstance(item, dict):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each service must be "
#                         "an object."
#                     ),
#                 )

#             service_id = item.get("id")

#             # IMPORTANT:
#             #
#             # Frontend must send:
#             #
#             # {
#             #     "id": "...",
#             #     "quantity": 1
#             # }
#             #
#             # NOT:
#             #
#             # {
#             #     "service_id": "...",
#             #     "quantity": 1
#             # }

#             if not service_id:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each service must "
#                         "contain an id."
#                     ),
#                 )

#             service_ids.append(
#                 str(service_id)
#             )

#         # =====================================================
#         # REMOVE DUPLICATE SERVICE IDS
#         # =====================================================

#         service_ids = list(
#             dict.fromkeys(service_ids)
#         )

#         # =====================================================
#         # GET SERVICES FROM DATABASE
#         # =====================================================

#         db_services = (
#             CustomerBookingRepository
#             .get_services_by_ids(
#                 service_ids
#             )
#         )

#         if not db_services:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Selected services were not found.",
#             )

#         db_service_map = {
#             str(service["id"]): service
#             for service in db_services
#         }

#         # =====================================================
#         # MAKE SURE EVERY REQUESTED SERVICE EXISTS
#         # =====================================================

#         for service_id in service_ids:

#             if service_id not in db_service_map:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         f"Service {service_id} "
#                         "was not found."
#                     ),
#                 )

#         # =====================================================
#         # EXTRACT SERVICE CATEGORIES
#         # =====================================================

#         service_categories = []

#         for service_id in service_ids:

#             service = (
#                 db_service_map[
#                     service_id
#                 ]
#             )

#             service_type = (
#                 service.get("service_type")
#             )

#             if not service_type:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         f"Service "
#                         f"{service.get('title', service_id)} "
#                         "does not have a service category."
#                     ),
#                 )

#             service_categories.append(
#                 str(service_type).strip()
#             )

#         # =====================================================
#         # UNIQUE CATEGORIES
#         # =====================================================

#         service_categories = list(
#             dict.fromkeys(
#                 service_categories
#             )
#         )

#         # =====================================================
#         # EXTRACT PINCODE FROM ADDRESS
#         # =====================================================
#         #
#         # For now we extract the first 6-digit pincode
#         # from full_address.
#         #
#         # Later, frontend can send pincode separately,
#         # which would be cleaner.
#         #

#         import re

#         pincode_match = re.search(
#             r"\b\d{6}\b",
#             full_address,
#         )

#         if not pincode_match:

#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "A valid 6-digit pincode "
#                     "is required in the address."
#                 ),
#             )

#         pincode = (
#             pincode_match.group(0)
#         )

#         # =====================================================
#         # SERVICE AVAILABILITY CHECK
#         # =====================================================
#         #
#         # This happens BEFORE creating the booking.
#         #
#         # Flow:
#         #
#         # pincode
#         #    ↓
#         # hub_locations
#         #    ↓
#         # hub
#         #    ↓
#         # hub_category_counts
#         #    ↓
#         # service category
#         #    ↓
#         # partner assigned?
#         #
#         # Only if everything passes do we create booking.
#         #

#         availability = (
#             CustomerBookingRepository
#             .check_service_availability(
#                 pincode=pincode,
#                 service_categories=service_categories,
#             )
#         )

#         if not availability.get(
#             "available"
#         ):

#             raise HTTPException(
#                 status_code=400,
#                 detail=availability.get(
#                     "message",
#                     "Service is not available in this area.",
#                 ),
#             )

#         # =====================================================
#         # GET ADD-ONS
#         # =====================================================

#         addon_ids = []

#         for item in add_ons or []:

#             if not isinstance(item, dict):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each add-on must "
#                         "be an object."
#                     ),
#                 )

#             addon_id = item.get("id")

#             if not addon_id:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Each add-on must "
#                         "contain an id."
#                     ),
#                 )

#             addon_ids.append(
#                 str(addon_id)
#             )

#         addon_ids = list(
#             dict.fromkeys(addon_ids)
#         )

#         db_addons = (
#             CustomerBookingRepository
#             .get_addons_by_ids(
#                 addon_ids
#             )
#         )

#         db_addon_map = {
#             str(addon["id"]): addon
#             for addon in db_addons
#         }

#         # =====================================================
#         # VALIDATE ADD-ONS
#         # =====================================================

#         for addon_id in addon_ids:

#             if addon_id not in db_addon_map:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         f"Add-on {addon_id} "
#                         "was not found or is inactive."
#                     ),
#                 )

#         # =====================================================
#         # CALCULATE TOTAL
#         # =====================================================
#         #
#         # IMPORTANT:
#         # Do NOT trust total_amount from frontend.
#         #
#         # Calculate it from database prices.
#         #

#         total_amount = 0.0

#         normalized_services = []

#         for item in services:

#             service_id = str(
#                 item["id"]
#             )

#             quantity = item.get(
#                 "quantity",
#                 1,
#             )

#             try:
#                 quantity = int(quantity)
#             except (
#                 ValueError,
#                 TypeError,
#             ):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Service quantity "
#                         "must be a number."
#                     ),
#                 )

#             if quantity <= 0:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Service quantity "
#                         "must be greater than zero."
#                     ),
#                 )

#             service = (
#                 db_service_map[
#                     service_id
#                 ]
#             )

#             price = float(
#                 service.get(
#                     "price"
#                 ) or 0
#             )

#             tax_percent = (
#                 service.get(
#                     "tax_percent"
#                 )
#             )

#             if isinstance(
#                 tax_percent,
#                 str,
#             ):

#                 tax_percent = (
#                     tax_percent
#                     .replace("%", "")
#                     .strip()
#                 )

#                 try:
#                     tax_percent = float(
#                         tax_percent
#                     )
#                 except (
#                     ValueError,
#                     TypeError,
#                 ):
#                     tax_percent = 0.0

#             elif tax_percent is None:

#                 tax_percent = 0.0

#             else:

#                 tax_percent = float(
#                     tax_percent
#                 )

#             base_amount = (
#                 price * quantity
#             )

#             tax_amount = (
#                 base_amount
#                 * tax_percent
#                 / 100
#             )

#             service_total = (
#                 base_amount
#                 + tax_amount
#             )

#             total_amount += (
#                 service_total
#             )

#             normalized_services.append(
#                 {
#                     "id": service_id,
#                     "quantity": quantity,
#                     "title": service.get(
#                         "title"
#                     ),
#                     "price": price,
#                     "tax_percent": tax_percent,
#                     "service_type": service.get(
#                         "service_type"
#                     ),
#                 }
#             )

#         # =====================================================
#         # ADD-ON TOTAL
#         # =====================================================

#         normalized_addons = []

#         for item in add_ons or []:

#             addon_id = str(
#                 item["id"]
#             )

#             quantity = item.get(
#                 "quantity",
#                 1,
#             )

#             try:
#                 quantity = int(quantity)
#             except (
#                 ValueError,
#                 TypeError,
#             ):
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Add-on quantity "
#                         "must be a number."
#                     ),
#                 )

#             if quantity <= 0:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=(
#                         "Add-on quantity "
#                         "must be greater than zero."
#                     ),
#                 )

#             addon = (
#                 db_addon_map[
#                     addon_id
#                 ]
#             )

#             price = float(
#                 addon.get(
#                     "price"
#                 ) or 0
#             )

#             addon_total = (
#                 price * quantity
#             )

#             total_amount += (
#                 addon_total
#             )

#             normalized_addons.append(
#                 {
#                     "id": addon_id,
#                     "quantity": quantity,
#                     "title": addon.get(
#                         "title"
#                     ),
#                     "price": price,
#                 }
#             )

#         # =====================================================
#         # ROUND TOTAL
#         # =====================================================

#         total_amount = round(
#             total_amount,
#             2,
#         )

#         if total_amount <= 0:
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Booking amount must "
#                     "be greater than zero."
#                 ),
#             )

#         # =====================================================
#         # CREATE BOOKING
#         # =====================================================

#         booking = (
#             CustomerBookingRepository
#             .create_booking(
#                 customer_name=customer_name,
#                 email=email,
#                 phone_number=phone_number,
#                 full_address=full_address,
#                 services=normalized_services,
#                 add_ons=normalized_addons,
#                 booking_date=str(
#                     booking_date
#                 ),
#                 booking_time=booking_time,
#                 total_amount=total_amount,
#                 user_id=user_id,
#                 latitude=latitude,
#                 longitude=longitude,
#                 location_link=location_link,
#             )
#         )

#         # =====================================================
#         # INSERT FAILED
#         # =====================================================

#         if not booking:

#             raise HTTPException(
#                 status_code=500,
#                 detail="Failed to create booking.",
#             )

#         # =====================================================
#         # RESPONSE
#         # =====================================================

#         return {
#             "success": True,

#             "booking_id": str(
#                 booking["id"]
#             ),

#             "message": (
#                 "Booking created successfully."
#             ),

#             "payment_status": booking.get(
#                 "payment_status",
#                 "pending",
#             ),

#             "payment_verified": bool(
#                 booking.get(
#                     "payment_verified",
#                     False,
#                 )
#             ),

#             "total_amount": total_amount,
#         }




















from datetime import date, datetime
import re

from fastapi import HTTPException, status

from app.repositories.customer_booking_repository import (
    CustomerBookingRepository,
)


class CustomerBookingService:

    # =========================================================
    # PRICE HELPER
    # =========================================================

    @staticmethod
    def _parse_price(value) -> float:

        if value is None:
            return 0.0

        try:
            return float(
                str(value)
                .replace("₹", "")
                .replace(",", "")
                .strip()
            )

        except (
            ValueError,
            TypeError,
        ):
            return 0.0

    # =========================================================
    # QUANTITY HELPER
    # =========================================================

    @staticmethod
    def _get_quantity(
        item: dict,
    ) -> int:

        quantity = item.get(
            "quantity",
            1,
        )

        try:
            quantity = int(quantity)

        except (
            ValueError,
            TypeError,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item quantity.",
            )

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero.",
            )

        return quantity

    # =========================================================
    # NORMALIZE BOOKING TIME
    # =========================================================

    @staticmethod
    def _normalize_booking_time(
        booking_time: str,
    ) -> str:
        """
        Normalize booking time before sending it to
        the database.

        Examples:

            05:30      -> 05:30 AM
            5:30       -> 05:30 AM
            17:30      -> 05:30 PM
            05:30 AM   -> 05:30 AM
            05:30 PM   -> 05:30 PM
            5:30 PM    -> 05:30 PM

        This prevents the database error:

            invalid value "05:30" for "am"
        """

        value = str(
            booking_time or ""
        ).strip()

        if not value:
            raise HTTPException(
                status_code=400,
                detail="Booking time is required.",
            )

        # -----------------------------------------------------
        # Already contains AM / PM
        # -----------------------------------------------------

        upper_value = value.upper()

        if upper_value.endswith("AM"):
            raw = value[:-2].strip()

            try:
                parsed = datetime.strptime(
                    raw,
                    "%H:%M",
                )

                return parsed.strftime(
                    "%I:%M AM"
                )

            except ValueError:
                try:
                    parsed = datetime.strptime(
                        raw,
                        "%I:%M",
                    )

                    return parsed.strftime(
                        "%I:%M AM"
                    )

                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "Invalid booking time. "
                            "Use HH:MM AM/PM."
                        ),
                    )

        if upper_value.endswith("PM"):
            raw = value[:-2].strip()

            try:
                parsed = datetime.strptime(
                    raw,
                    "%H:%M",
                )

                return parsed.strftime(
                    "%I:%M PM"
                )

            except ValueError:
                try:
                    parsed = datetime.strptime(
                        raw,
                        "%I:%M",
                    )

                    return parsed.strftime(
                        "%I:%M PM"
                    )

                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "Invalid booking time. "
                            "Use HH:MM AM/PM."
                        ),
                    )

        # -----------------------------------------------------
        # 24-hour time
        # -----------------------------------------------------

        try:
            parsed = datetime.strptime(
                value,
                "%H:%M",
            )

            return parsed.strftime(
                "%I:%M %p"
            )

        except ValueError:
            pass

        # -----------------------------------------------------
        # 12-hour time without AM/PM is ambiguous.
        # We treat it as AM.
        # -----------------------------------------------------

        try:
            parsed = datetime.strptime(
                value,
                "%I:%M",
            )

            return parsed.strftime(
                "%I:%M AM"
            )

        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid booking time. "
                    "Use HH:MM or HH:MM AM/PM."
                ),
            )

    # =========================================================
    # EXTRACT PINCODE
    # =========================================================

    @staticmethod
    def _extract_pincode(
        full_address: str,
    ) -> str:

        match = re.search(
            r"\b\d{6}\b",
            full_address,
        )

        if not match:
            raise HTTPException(
                status_code=400,
                detail=(
                    "A valid 6-digit pincode "
                    "is required in the address."
                ),
            )

        return match.group(0)

    # =========================================================
    # CHECK SERVICE AVAILABILITY
    # =========================================================

    @staticmethod
    def check_service_availability(
        pincode: str,
        service_categories: list[str],
    ):
        """
        Service availability flow:

            PINCODE
            ↓
            neatify_service_areas
            ↓
            hub_locations
            ↓
            hub
            ↓
            hub_category_counts
            ↓
            category + partner count
            ↓
            AVAILABLE / PARTNER_NOT_AVAILABLE

        Important:
            - neatify_service_areas determines whether the
            pincode is a valid Neatify service area.
            - hub_locations determines which hub serves the
            pincode.
            - hub_category_counts determines whether the
            requested category has partners in that hub.
        """

        pincode = str(pincode).strip()

        # =====================================================
        # STEP 1
        # PINCODE → NEATIFY SERVICE AREAS
        # =====================================================

        service_areas = (
            CustomerBookingRepository
            .get_service_areas_by_pincode(
                pincode=pincode,
            )
        )

        # -----------------------------------------------------
        # PINCODE DOES NOT EXIST IN SERVICE AREAS
        # -----------------------------------------------------

        # if not service_areas:
        #     return {
        #         "available": False,
        #         "reason": "SERVICE_AREA_NOT_AVAILABLE",
        #         "message": (
        #             "Service is not available "
        #             "in this area."
        #         ),
        #         "pincode": pincode,
        #         "hub": None,
        #         "location": None,
        #         "service_area": [],
        #         "services": [],
        #     }

        # =====================================================
        # STEP 2
        # GET HUB(S) FOR PINCODE
        # =====================================================

        hub_locations = (
            CustomerBookingRepository
            .get_hub_locations_by_pincode(
                pincode=pincode,
            )
        )

        # -----------------------------------------------------
        # SERVICE AREA EXISTS BUT NO HUB IS MAPPED
        # -----------------------------------------------------

        if not hub_locations:
            return {
                "available": False,
                "reason": "SERVICE_AREA_NOT_AVAILABLE",
                "message": (
                    "Service is not available "
                    "in this area."
                ),
                "pincode": pincode,
                "hub": None,
                "location": None,
                "service_area": service_areas,
                "services": [],
            }

        # =====================================================
        # STEP 3
        # VALIDATE SERVICE CATEGORIES
        # =====================================================

        checked_services = []

        for category in service_categories:

            category = str(
                category or ""
            ).strip()

            # -------------------------------------------------
            # INVALID CATEGORY
            # -------------------------------------------------

            if not category:
                return {
                    "available": False,
                    "reason": "INVALID_SERVICE_CATEGORY",
                    "message": (
                        "A selected service has "
                        "no service category."
                    ),
                    "pincode": pincode,
                    "hub": None,
                    "location": None,
                    "service_area": service_areas,
                    "services": checked_services,
                }

            # =================================================
            # STEP 4
            # CHECK CATEGORY IN EACH HUB FOR THIS PINCODE
            # =================================================

            category_available = False
            matched_record = None
            matched_hub_location = None

            for hub_location in hub_locations:

                hub_name = str(
                    hub_location.get("hub_name") or ""
                ).strip()

                if not hub_name:
                    continue

                # -------------------------------------------------
                # GET CATEGORY RECORDS FOR THIS HUB
                # -------------------------------------------------

                records = (
                    CustomerBookingRepository
                    .get_hub_category_records(
                        category=category,
                    )
                )

                # -------------------------------------------------
                # FIND RECORD BELONGING TO THIS HUB
                # -------------------------------------------------

                for record in records:

                    record_hub = str(
                        record.get("hub") or ""
                    ).strip().lower()

                    if record_hub != hub_name.lower():
                        continue

                    # ---------------------------------------------
                    # PARTNER COUNT
                    # ---------------------------------------------

                    try:
                        partner_count = int(
                            record.get("count") or 0
                        )
                    except (
                        ValueError,
                        TypeError,
                    ):
                        partner_count = 0

                    # ---------------------------------------------
                    # ASSIGNED STAFF
                    # ---------------------------------------------

                    assigned_staff = str(
                        record.get("assigned_staff") or ""
                    ).strip()

                    # ---------------------------------------------
                    # CATEGORY IS AVAILABLE
                    #
                    # count > 0 AND assigned staff exists
                    # ---------------------------------------------

                    if (
                        partner_count > 0
                        # and assigned_staff
                    ):
                        category_available = True
                        matched_record = record
                        matched_hub_location = hub_location
                        break

                if category_available:
                    break

            # =================================================
            # STEP 5
            # PARTNER NOT AVAILABLE
            # =================================================

            if not category_available:

                # We know:
                #   ✔ pincode exists in service area
                #   ✔ pincode has a valid hub
                #
                # Therefore this is NOT a service-area problem.
                #
                # It means the requested category has no
                # available partner in that hub.

                primary_hub = hub_locations[0]

                return {
                    "available": False,
                    "reason": "PARTNER_NOT_AVAILABLE",
                    "message": (
                        "Partner is not available "
                        "for this service in your area."
                    ),
                    "pincode": pincode,
                    "hub": primary_hub.get("hub_name"),
                    "location": primary_hub.get(
                        "location_name"
                    ),
                    "service_area": service_areas,
                    "services": checked_services,
                }

            # =================================================
            # STEP 6
            # SUCCESS FOR THIS CATEGORY
            # =================================================

            partner_count = int(
                matched_record.get("count") or 0
            )

            matched_hub = str(
                matched_record.get("hub") or ""
            ).strip()

            matched_location = str(
                matched_hub_location.get(
                    "location_name"
                ) or ""
            ).strip()

            checked_services.append(
                {
                    "category": category,
                    "available": True,
                    "partner_count": partner_count,
                    "assigned_staff": str(
                        matched_record.get(
                            "assigned_staff"
                        ) or ""
                    ).strip(),
                }
            )

        # =====================================================
        # STEP 7
        # EVERYTHING AVAILABLE
        # =====================================================

        if not checked_services:
            return {
                "available": False,
                "reason": "INVALID_SERVICE_CATEGORY",
                "message": (
                    "No service category was selected."
                ),
                "pincode": pincode,
                "hub": None,
                "location": None,
                "service_area": service_areas,
                "services": [],
            }

        # Use the hub/location from the first successful
        # category resolution.

        first_available_category = checked_services[0]

        final_hub = None
        final_location = None

        # Resolve the first successful category again so that
        # the response contains the actual matching hub.
        category = first_available_category["category"]

        for hub_location in hub_locations:

            hub_name = str(
                hub_location.get("hub_name") or ""
            ).strip()

            records = (
                CustomerBookingRepository
                .get_hub_category_records(
                    category=category,
                )
            )

            for record in records:

                record_hub = str(
                    record.get("hub") or ""
                ).strip()

                if record_hub.lower() != hub_name.lower():
                    continue

                try:
                    partner_count = int(
                        record.get("count") or 0
                    )
                except (
                    ValueError,
                    TypeError,
                ):
                    partner_count = 0

                assigned_staff = str(
                    record.get("assigned_staff") or ""
                ).strip()

                if (
                    partner_count > 0
                    # and assigned_staff
                ):
                    final_hub = hub_name
                    final_location = str(
                        hub_location.get(
                            "location_name"
                        ) or ""
                    ).strip()
                    break

            if final_hub:
                break

        return {
            "available": True,
            "reason": "AVAILABLE",
            "message": (
                "Service is available "
                "in this area."
            ),
            "pincode": pincode,
            "hub": final_hub,
            "location": final_location,
            "service_area": service_areas,
            "services": checked_services,
        }

    # =========================================================
    # CREATE BOOKING
    # =========================================================

    @staticmethod
    def create_booking(
        user_id: str,
        customer_name: str,
        email: str,
        phone_number: str,
        full_address: str,
        services,
        booking_date,
        booking_time: str,
        add_ons=None,
        latitude=None,
        longitude=None,
        location_link=None,
    ):

        # =====================================================
        # BASIC VALIDATION
        # =====================================================

        customer_name = str(
            customer_name
        ).strip()

        email = str(
            email
        ).strip()

        phone_number = str(
            phone_number
        ).strip()

        full_address = str(
            full_address
        ).strip()

        if not customer_name:
            raise HTTPException(
                status_code=400,
                detail="Customer name is required.",
            )

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Email is required.",
            )

        if not phone_number:
            raise HTTPException(
                status_code=400,
                detail="Phone number is required.",
            )

        if not full_address:
            raise HTTPException(
                status_code=400,
                detail="Address is required.",
            )

        # =====================================================
        # NORMALIZE TIME
        # =====================================================

        booking_time = (
            CustomerBookingService
            ._normalize_booking_time(
                booking_time
            )
        )

        # =====================================================
        # DATE VALIDATION
        # =====================================================

        if isinstance(
            booking_date,
            str,
        ):

            try:
                booking_date = date.fromisoformat(
                    booking_date
                )

            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Invalid booking date. "
                        "Use YYYY-MM-DD."
                    ),
                )

        if not isinstance(
            booking_date,
            date,
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid booking date.",
            )

        if booking_date < date.today():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Booking date cannot "
                    "be in the past."
                ),
            )

        # =====================================================
        # SERVICES VALIDATION
        # =====================================================

        if not services:

            raise HTTPException(
                status_code=400,
                detail=(
                    "At least one service "
                    "is required."
                ),
            )

        service_ids = []

        for item in services:

            if not isinstance(
                item,
                dict,
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each service must "
                        "be an object."
                    ),
                )

            service_id = item.get(
                "id"
            )

            if not service_id:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each service must "
                        "contain an id."
                    ),
                )

            service_ids.append(
                str(service_id)
            )

        # =====================================================
        # DUPLICATE SERVICES
        # =====================================================

        if len(service_ids) != len(
            set(service_ids)
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Duplicate services "
                    "are not allowed."
                ),
            )

        # =====================================================
        # GET SERVICES
        # =====================================================

        db_services = (
            CustomerBookingRepository
            .get_services_by_ids(
                service_ids
            )
        )

        if len(db_services) != len(
            service_ids
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "One or more selected "
                    "services are invalid."
                ),
            )

        service_map = {
            str(service["id"]): service
            for service in db_services
        }

        # =====================================================
        # EXTRACT CATEGORIES
        # =====================================================

        service_categories = []

        for service_id in service_ids:

            service = service_map[
                service_id
            ]

            service_type = (
                service.get(
                    "service_type"
                )
            )

            if not service_type:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Service "
                        f"{service.get('title', service_id)} "
                        "does not have a service category."
                    ),
                )

            service_categories.append(
                str(
                    service_type
                ).strip()
            )

        service_categories = list(
            dict.fromkeys(
                service_categories
            )
        )

        # =====================================================
        # EXTRACT PINCODE
        # =====================================================

        pincode = (
            CustomerBookingService
            ._extract_pincode(
                full_address
            )
        )

        # =====================================================
        # SERVICE AVAILABILITY
        # =====================================================
        #
        # IMPORTANT:
        #
        # This happens BEFORE booking creation.
        #
        # pincode
        #    ↓
        # hub_locations
        #    ↓
        # hub + location
        #    ↓
        # hub_category_counts
        #    ↓
        # category
        #    ↓
        # partner available
        #    ↓
        # CREATE BOOKING
        #

        availability = (
            CustomerBookingService
            .check_service_availability(
                pincode=pincode,
                service_categories=(
                    service_categories
                ),
            )
        )

        if not availability.get(
            "available"
        ):

            raise HTTPException(
                status_code=400,
                detail={
                    "code": availability.get(
                        "reason",
                        "SERVICE_NOT_AVAILABLE",
                    ),
                    "message": availability.get(
                        "message",
                        "Service is not available.",
                    ),
                    "pincode": availability.get(
                        "pincode"
                    ),
                    "hub": availability.get(
                        "hub"
                    ),
                    "location": availability.get(
                        "location"
                    ),
                },
            )

        hub_name = availability.get(
            "hub"
        )

        location_name = availability.get(
            "location"
        )

        # =====================================================
        # ADD-ONS VALIDATION
        # =====================================================

        add_ons = add_ons or []

        addon_ids = []

        for item in add_ons:

            if not isinstance(
                item,
                dict,
            ):

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each add-on must "
                        "be an object."
                    ),
                )

            addon_id = item.get(
                "id"
            )

            if not addon_id:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each add-on must "
                        "contain an id."
                    ),
                )

            addon_ids.append(
                str(addon_id)
            )

        # =====================================================
        # DUPLICATE ADD-ONS
        # =====================================================

        if len(addon_ids) != len(
            set(addon_ids)
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Duplicate add-ons "
                    "are not allowed."
                ),
            )

        # =====================================================
        # GET ADD-ONS
        # =====================================================

        db_addons = []

        if addon_ids:

            db_addons = (
                CustomerBookingRepository
                .get_addons_by_ids(
                    addon_ids
                )
            )

            if len(db_addons) != len(
                addon_ids
            ):

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "One or more selected "
                        "add-ons are invalid."
                    ),
                )

        addon_map = {
            str(addon["id"]): addon
            for addon in db_addons
        }

        # =====================================================
        # CALCULATE TOTAL
        # =====================================================

        calculated_total = 0.0

        normalized_services = []

        # =====================================================
        # SERVICES
        # =====================================================

        for item in services:

            service_id = str(
                item["id"]
            )

            quantity = (
                CustomerBookingService
                ._get_quantity(
                    item
                )
            )

            service = service_map[
                service_id
            ]

            price = (
                CustomerBookingService
                ._parse_price(
                    service.get(
                        "price"
                    )
                )
            )

            if price <= 0:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid service price "
                        f"for '{service.get('title')}'."
                    ),
                )

            line_total = (
                price * quantity
            )

            calculated_total += (
                line_total
            )

            normalized_services.append(
                {
                    "id": service_id,
                    "title": service.get(
                        "title"
                    ),
                    "quantity": quantity,
                    "price": price,
                }
            )

        # =====================================================
        # ADD-ONS
        # =====================================================

        normalized_addons = []

        for item in add_ons:

            addon_id = str(
                item["id"]
            )

            quantity = (
                CustomerBookingService
                ._get_quantity(
                    item
                )
            )

            addon = addon_map[
                addon_id
            ]

            price = (
                CustomerBookingService
                ._parse_price(
                    addon.get(
                        "price"
                    )
                )
            )

            if price <= 0:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid add-on price "
                        f"for '{addon.get('title')}'."
                    ),
                )

            line_total = (
                price * quantity
            )

            calculated_total += (
                line_total
            )

            normalized_addons.append(
                {
                    "id": addon_id,
                    "title": addon.get(
                        "title"
                    ),
                    "quantity": quantity,
                    "price": price,
                }
            )

        # =====================================================
        # FINAL TOTAL
        # =====================================================

        calculated_total = round(
            calculated_total,
            2,
        )

        if calculated_total <= 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Booking amount must "
                    "be greater than zero."
                ),
            )

        # =====================================================
        # STORE ADD-ONS INSIDE SERVICES JSON
        # =====================================================
        #
        # Your bookings table does NOT have an add_ons
        # column according to the schema you provided.
        #
        # Therefore we keep the existing services JSON
        # structure and append add-ons as a separate key.
        #

        booking_services = {
            "services": normalized_services,
            "add_ons": normalized_addons,
        }

        # =====================================================
        # CREATE BOOKING
        # =====================================================

        booking = (
            CustomerBookingRepository
            .create_booking(
                customer_name=customer_name,

                email=email,

                phone_number=phone_number,

                full_address=full_address,

                services=booking_services,

                booking_date=(
                    booking_date.isoformat()
                ),

                booking_time=booking_time,

                total_amount=calculated_total,

                user_id=user_id,

                latitude=latitude,

                longitude=longitude,

                location_link=location_link,

                hub_name=hub_name,
            )
        )

        # =====================================================
        # INSERT FAILURE
        # =====================================================

        if not booking:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to create booking."
                ),
            )

        # =====================================================
        # RESPONSE
        # =====================================================

        return {
            "success": True,

            "booking_id": str(
                booking["id"]
            ),

            "message": (
                "Booking created successfully."
            ),

            "payment_status": booking.get(
                "payment_status",
                "pending",
            ),

            "payment_verified": bool(
                booking.get(
                    "payment_verified",
                    False,
                )
            ),

            "total_amount": float(
                booking.get(
                    "total_amount",
                    calculated_total,
                )
            ),
        }

    # =========================================================
    # GET CUSTOMER BOOKINGS
    # =========================================================

    @staticmethod
    def get_customer_bookings(
        user_id: str,
    ):

        return (
            CustomerBookingRepository
            .get_customer_bookings(
                user_id=user_id
            )
        ) 

# =========================================================
# GET SINGLE CUSTOMER BOOKING
# =========================================================

@staticmethod
def get_booking(
    booking_id: str,
    user_id: str,
):
    booking = (
        CustomerBookingRepository
        .get_booking(
            booking_id=booking_id,
            user_id=user_id,
        )
    )

    if not booking:
        raise ValueError(
            "Booking not found."
        )

    return booking