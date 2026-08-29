# from app.supabase.client import supabase


# class CustomerBookingRepository:

#     # =========================================================
#     # CREATE BOOKING
#     # =========================================================

#     @staticmethod
#     def create_booking(
#         customer_name: str,
#         email: str,
#         phone_number: str,
#         full_address: str,
#         services,
#         booking_date: str,
#         booking_time: str,
#         total_amount: float,
#         user_id: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .insert(
#                 {
#                     "customer_name": customer_name,
#                     "email": email,
#                     "phone_number": phone_number,
#                     "full_address": full_address,
#                     "services": services,
#                     "booking_date": booking_date,
#                     "booking_time": booking_time,
#                     "total_amount": total_amount,
#                     "user_id": user_id,

#                     # Payment starts as unpaid.
#                     "payment_status": "pending",
#                     "payment_verified": False,
#                 }
#             )
#             .execute()
#         )

#         return response.data[0] if response.data else None

#     # =========================================================
#     # GET BOOKING
#     # =========================================================

#     @staticmethod
#     def get_booking(
#         booking_id: str,
#         user_id: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("id", booking_id)
#             .eq("user_id", user_id)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # UPDATE RAZORPAY ORDER
#     # =========================================================

#     @staticmethod
#     def set_razorpay_order(
#         booking_id: str,
#         user_id: str,
#         razorpay_order_id: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "razorpay_order_id": razorpay_order_id,
#                     "payment_status": "pending",
#                     "payment_verified": False,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("user_id", user_id)
#             .execute()
#         )

#         return response.data[0] if response.data else None

#     # =========================================================
#     # MARK PAYMENT SUCCESS
#     # =========================================================

#     @staticmethod
#     def mark_payment_success(
#         booking_id: str,
#         user_id: str,
#         razorpay_order_id: str,
#         razorpay_payment_id: str,
#         razorpay_signature: str,
#         payment_method: str | None = None,
#     ):

#         update_data = {
#             "razorpay_order_id": razorpay_order_id,
#             "razorpay_payment_id": razorpay_payment_id,
#             "razorpay_signature": razorpay_signature,
#             "payment_status": "paid",
#             "payment_verified": True,
#         }

#         if payment_method:
#             update_data["payment_method"] = payment_method

#         response = (
#             supabase
#             .table("bookings")
#             .update(update_data)
#             .eq("id", booking_id)
#             .eq("user_id", user_id)
#             .execute()
#         )

#         return response.data[0] if response.data else None

#     # =========================================================
#     # MARK PAYMENT FAILED
#     # =========================================================

#     @staticmethod
#     def mark_payment_failed(
#         booking_id: str,
#         user_id: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 {
#                     "payment_status": "failed",
#                     "payment_verified": False,
#                 }
#             )
#             .eq("id", booking_id)
#             .eq("user_id", user_id)
#             .execute()
#         )

#         return response.data[0] if response.data else None






















from app.supabase.client import supabase


class CustomerBookingRepository:

    # =========================================================
    # GET SERVICES BY IDS
    # =========================================================

    @staticmethod
    def get_services_by_ids(
        service_ids: list[str],
    ):

        if not service_ids:
            return []

        response = (
            supabase
            .table("services")
            .select(
                "id, title, price, tax_percent"
            )
            .in_(
                "id",
                service_ids,
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # GET ADD-ONS BY IDS
    # =========================================================

    @staticmethod
    def get_addons_by_ids(
        addon_ids: list[str],
    ):

        if not addon_ids:
            return []

        response = (
            supabase
            .table("add_ons")
            .select(
                "id, title, price"
            )
            .in_(
                "id",
                addon_ids,
            )
            .eq(
                "is_active",
                True,
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # CREATE BOOKING
    # =========================================================

    @staticmethod
    def create_booking(
        customer_name: str,
        email: str,
        phone_number: str,
        full_address: str,
        services,
        add_ons,
        booking_date: str,
        booking_time: str,
        total_amount: float,
        user_id: str,
        latitude: float | None = None,
        longitude: float | None = None,
        location_link: str | None = None,
    ):

        insert_data = {
            "customer_name": customer_name,

            "email": email,

            "phone_number": phone_number,

            "full_address": full_address,

            "services": services,

            "booking_date": booking_date,

            "booking_time": booking_time,

            "total_amount": total_amount,

            "user_id": user_id,

            "payment_status": "pending",

            "payment_verified": False,
        }

        # =====================================================
        # ADD-ONS
        # =====================================================

        # Only add this if your bookings table has
        # an "add_ons" JSON/JSONB column.
        #
        # If the column exists, this will store the
        # normalized add-ons separately.

        if add_ons:
            insert_data["add_ons"] = add_ons

        # =====================================================
        # LOCATION
        # =====================================================

        if latitude is not None:
            insert_data["latitude"] = latitude

        if longitude is not None:
            insert_data["longitude"] = longitude

        if location_link:
            insert_data["location_link"] = (
                location_link
            )

        # =====================================================
        # INSERT
        # =====================================================

        response = (
            supabase
            .table("bookings")
            .insert(
                insert_data
            )
            .execute()
        )

        return (
            response.data[0]
            if response.data
            else None
        )

    # =========================================================
    # GET BOOKING
    # =========================================================

    @staticmethod
    def get_booking(
        booking_id: str,
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .select("*")
            .eq(
                "id",
                booking_id,
            )
            .eq(
                "user_id",
                user_id,
            )
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # UPDATE RAZORPAY ORDER
    # =========================================================

    @staticmethod
    def set_razorpay_order(
        booking_id: str,
        user_id: str,
        razorpay_order_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "razorpay_order_id":
                        razorpay_order_id,

                    "payment_status":
                        "pending",

                    "payment_verified":
                        False,
                }
            )
            .eq(
                "id",
                booking_id,
            )
            .eq(
                "user_id",
                user_id,
            )
            .execute()
        )

        return (
            response.data[0]
            if response.data
            else None
        )

    # =========================================================
    # MARK PAYMENT SUCCESS
    # =========================================================

    @staticmethod
    def mark_payment_success(
        booking_id: str,
        user_id: str,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
        payment_method: str | None = None,
    ):

        update_data = {
            "razorpay_order_id":
                razorpay_order_id,

            "razorpay_payment_id":
                razorpay_payment_id,

            "razorpay_signature":
                razorpay_signature,

            "payment_status":
                "paid",

            "payment_verified":
                True,
        }

        if payment_method:
            update_data[
                "payment_method"
            ] = payment_method

        response = (
            supabase
            .table("bookings")
            .update(
                update_data
            )
            .eq(
                "id",
                booking_id,
            )
            .eq(
                "user_id",
                user_id,
            )
            .execute()
        )

        return (
            response.data[0]
            if response.data
            else None
        )

    # =========================================================
    # MARK PAYMENT FAILED
    # =========================================================

    @staticmethod
    def mark_payment_failed(
        booking_id: str,
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "payment_status":
                        "failed",

                    "payment_verified":
                        False,
                }
            )
            .eq(
                "id",
                booking_id,
            )
            .eq(
                "user_id",
                user_id,
            )
            .execute()
        )

        return (
            response.data[0]
            if response.data
            else None
        )