# from fastapi import HTTPException, status

# from app.repositories.customer_booking_repository import (
#     CustomerBookingRepository,
# )


# class CustomerBookingService:

#     @staticmethod
#     def create_booking(
#         user_id: str,
#         customer_name: str,
#         email: str,
#         phone_number: str,
#         full_address: str,
#         services,
#         booking_date: str,
#         booking_time: str,
#         total_amount: float,
#     ):

#         customer_name = customer_name.strip()
#         email = email.strip()
#         phone_number = phone_number.strip()
#         full_address = full_address.strip()

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

#         if total_amount <= 0:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Booking amount must be greater than zero.",
#             )

#         booking = (
#             CustomerBookingRepository
#             .create_booking(
#                 customer_name=customer_name,
#                 email=email,
#                 phone_number=phone_number,
#                 full_address=full_address,
#                 services=services,
#                 booking_date=booking_date,
#                 booking_time=booking_time,
#                 total_amount=total_amount,
#                 user_id=user_id,
#             )
#         )

#         if not booking:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to create booking.",
#             )

#         return {
#             "success": True,
#             "booking_id": str(booking["id"]),
#             "message": "Booking created successfully.",
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
#         }

















from datetime import date

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

        except (ValueError, TypeError):
            return 0.0

    # =========================================================
    # QUANTITY HELPER
    # =========================================================

    @staticmethod
    def _get_quantity(item: dict) -> int:

        quantity = item.get(
            "quantity",
            1,
        )

        try:
            quantity = int(quantity)

        except (ValueError, TypeError):
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

        customer_name = customer_name.strip()
        email = email.strip()
        phone_number = phone_number.strip()
        full_address = full_address.strip()
        booking_time = booking_time.strip()

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

        if not booking_time:
            raise HTTPException(
                status_code=400,
                detail="Booking time is required.",
            )

        # =====================================================
        # DATE VALIDATION
        # =====================================================

        if isinstance(booking_date, str):

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

        if not isinstance(booking_date, date):
            raise HTTPException(
                status_code=400,
                detail="Invalid booking date.",
            )

        if booking_date < date.today():
            raise HTTPException(
                status_code=400,
                detail="Booking date cannot be in the past.",
            )

        # =====================================================
        # SERVICES VALIDATION
        # =====================================================

        if not services:
            raise HTTPException(
                status_code=400,
                detail="At least one service is required.",
            )

        service_ids = []

        for item in services:

            if not isinstance(item, dict):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each service must be an object."
                    ),
                )

            service_id = item.get("id")

            if not service_id:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each service must contain an id."
                    ),
                )

            service_ids.append(
                str(service_id)
            )

        # Prevent duplicate services.
        if len(service_ids) != len(set(service_ids)):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Duplicate services are not allowed."
                ),
            )

        # =====================================================
        # GET SERVICES FROM DATABASE
        # =====================================================

        db_services = (
            CustomerBookingRepository
            .get_services_by_ids(
                service_ids
            )
        )

        if len(db_services) != len(service_ids):
            raise HTTPException(
                status_code=400,
                detail=(
                    "One or more selected services "
                    "are invalid."
                ),
            )

        service_map = {
            str(service["id"]): service
            for service in db_services
        }

        # =====================================================
        # ADD-ONS VALIDATION
        # =====================================================

        add_ons = add_ons or []

        addon_ids = []

        for item in add_ons:

            if not isinstance(item, dict):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each add-on must be an object."
                    ),
                )

            addon_id = item.get("id")

            if not addon_id:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Each add-on must contain an id."
                    ),
                )

            addon_ids.append(
                str(addon_id)
            )

        # Prevent duplicate add-ons.
        if len(addon_ids) != len(set(addon_ids)):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Duplicate add-ons are not allowed."
                ),
            )

        db_addons = []

        if addon_ids:

            db_addons = (
                CustomerBookingRepository
                .get_addons_by_ids(
                    addon_ids
                )
            )

            if len(db_addons) != len(addon_ids):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "One or more selected add-ons "
                        "are invalid."
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
                ._get_quantity(item)
            )

            service = service_map[
                service_id
            ]

            price = (
                CustomerBookingService
                ._parse_price(
                    service.get("price")
                )
            )

            if price <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid service price for "
                        f"'{service.get('title')}'."
                    ),
                )

            line_total = (
                price * quantity
            )

            calculated_total += line_total

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
                ._get_quantity(item)
            )

            addon = addon_map[
                addon_id
            ]

            price = (
                CustomerBookingService
                ._parse_price(
                    addon.get("price")
                )
            )

            if price <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid add-on price for "
                        f"'{addon.get('title')}'."
                    ),
                )

            line_total = (
                price * quantity
            )

            calculated_total += line_total

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
                    "Booking amount must be "
                    "greater than zero."
                ),
            )

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

                services=normalized_services,

                add_ons=normalized_addons,

                booking_date=booking_date.isoformat(),

                booking_time=booking_time,

                total_amount=calculated_total,

                user_id=user_id,

                latitude=latitude,

                longitude=longitude,

                location_link=location_link,
            )
        )

        # =====================================================
        # INSERT FAILURE
        # =====================================================

        if not booking:
            raise HTTPException(
                status_code=500,
                detail="Failed to create booking.",
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