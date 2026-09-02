# from app.supabase.client import supabase


# class CustomerBookingRepository:

#     # =========================================================
#     # GET SERVICES BY IDS
#     # =========================================================

#     @staticmethod
#     def get_services_by_ids(
#         service_ids: list[str],
#     ):

#         if not service_ids:
#             return []

#         response = (
#             supabase
#             .table("services")
#             .select(
#                 "id, title, price, tax_percent"
#             )
#             .in_(
#                 "id",
#                 service_ids,
#             )
#             .execute()
#         )

#         return response.data or []

#     # =========================================================
#     # GET ADD-ONS BY IDS
#     # =========================================================

#     @staticmethod
#     def get_addons_by_ids(
#         addon_ids: list[str],
#     ):

#         if not addon_ids:
#             return []

#         response = (
#             supabase
#             .table("add_ons")
#             .select(
#                 "id, title, price"
#             )
#             .in_(
#                 "id",
#                 addon_ids,
#             )
#             .eq(
#                 "is_active",
#                 True,
#             )
#             .execute()
#         )

#         return response.data or []

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
#         add_ons,
#         booking_date: str,
#         booking_time: str,
#         total_amount: float,
#         user_id: str,
#         latitude: float | None = None,
#         longitude: float | None = None,
#         location_link: str | None = None,
#     ):

#         insert_data = {
#             "customer_name": customer_name,

#             "email": email,

#             "phone_number": phone_number,

#             "full_address": full_address,

#             "services": services,

#             "booking_date": booking_date,

#             "booking_time": booking_time,

#             "total_amount": total_amount,

#             "user_id": user_id,

#             "payment_status": "pending",

#             "payment_verified": False,
#         }

#         # =====================================================
#         # ADD-ONS
#         # =====================================================

#         # Only add this if your bookings table has
#         # an "add_ons" JSON/JSONB column.
#         #
#         # If the column exists, this will store the
#         # normalized add-ons separately.

#         if add_ons:
#             insert_data["add_ons"] = add_ons

#         # =====================================================
#         # LOCATION
#         # =====================================================

#         if latitude is not None:
#             insert_data["latitude"] = latitude

#         if longitude is not None:
#             insert_data["longitude"] = longitude

#         if location_link:
#             insert_data["location_link"] = (
#                 location_link
#             )

#         # =====================================================
#         # INSERT
#         # =====================================================

#         response = (
#             supabase
#             .table("bookings")
#             .insert(
#                 insert_data
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

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
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
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
#                     "razorpay_order_id":
#                         razorpay_order_id,

#                     "payment_status":
#                         "pending",

#                     "payment_verified":
#                         False,
#                 }
#             )
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )
#         # =========================================================
#     # GET CUSTOMER BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_customer_bookings(
#         user_id: str,
#     ):
#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq("user_id", user_id)
#             .order("created_at", desc=True)
#             .execute()
#         )

#         return response.data or []

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
#             "razorpay_order_id":
#                 razorpay_order_id,

#             "razorpay_payment_id":
#                 razorpay_payment_id,

#             "razorpay_signature":
#                 razorpay_signature,

#             "payment_status":
#                 "paid",

#             "payment_verified":
#                 True,
#         }

#         if payment_method:
#             update_data[
#                 "payment_method"
#             ] = payment_method

#         response = (
#             supabase
#             .table("bookings")
#             .update(
#                 update_data
#             )
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

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
#                     "payment_status":
#                         "failed",

#                     "payment_verified":
#                         False,
#                 }
#             )
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )



















# from app.supabase.client import supabase


# class CustomerBookingRepository:

#     # =========================================================
#     # GET SERVICES BY IDS
#     # =========================================================

#     @staticmethod
#     def get_services_by_ids(
#         service_ids: list[str],
#     ):
#         if not service_ids:
#             return []

#         response = (
#             supabase
#             .table("services")
#             .select(
#                 """
#                 id,
#                 title,
#                 price,
#                 tax_percent,
#                 service_type
#                 """
#             )
#             .in_(
#                 "id",
#                 service_ids,
#             )
#             .execute()
#         )

#         return response.data or []

#     # =========================================================
#     # GET ADD-ONS BY IDS
#     # =========================================================

#     @staticmethod
#     def get_addons_by_ids(
#         addon_ids: list[str],
#     ):
#         if not addon_ids:
#             return []

#         response = (
#             supabase
#             .table("add_ons")
#             .select(
#                 """
#                 id,
#                 title,
#                 price
#                 """
#             )
#             .in_(
#                 "id",
#                 addon_ids,
#             )
#             .eq(
#                 "is_active",
#                 True,
#             )
#             .execute()
#         )

#         return response.data or []

#     # =========================================================
#     # FIND HUB LOCATION BY PINCODE
#     # =========================================================

#     @staticmethod
#     def get_hub_location_by_pincode(
#         pincode: str,
#     ):
#         """
#         Find active hub/location using customer pincode.

#         Source:
#             hub_locations
#         """

#         response = (
#             supabase
#             .table("hub_locations")
#             .select(
#                 """
#                 id,
#                 hub_name,
#                 location_name,
#                 pincode,
#                 is_active
#                 """
#             )
#             .eq(
#                 "pincode",
#                 str(pincode).strip(),
#             )
#             .eq(
#                 "is_active",
#                 True,
#             )
#             .limit(1)
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

#     # =========================================================
#     # FIND NEATIFY SERVICE AREA BY PINCODE
#     # =========================================================

#     @staticmethod
#     def get_service_area_by_pincode(
#         pincode: str,
#     ):
#         """
#         Check whether the pincode exists in
#         neatify_service_areas.
#         """

#         response = (
#             supabase
#             .table("neatify_service_areas")
#             .select(
#                 """
#                 id,
#                 area_name,
#                 pincode
#                 """
#             )
#             .eq(
#                 "pincode",
#                 str(pincode).strip(),
#             )
#             .limit(1)
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

#     # =========================================================
#     # CHECK HUB CATEGORY / PARTNER AVAILABILITY
#     # =========================================================

#     @staticmethod
#     def get_hub_category_record(
#         hub_name: str,
#         category: str,
#     ):
#         """
#         Check hub_category_counts.

#         A category is considered available only when:

#             count > 0

#         AND

#             assigned_staff is not empty.
#         """

#         response = (
#             supabase
#             .table("hub_category_counts")
#             .select(
#                 """
#                 id,
#                 hub,
#                 location,
#                 category,
#                 count,
#                 assigned_staff
#                 """
#             )
#             .eq(
#                 "hub",
#                 hub_name,
#             )
#             .eq(
#                 "category",
#                 category,
#             )
#             .limit(1)
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

#     # =========================================================
#     # CHECK SERVICE AVAILABILITY
#     # =========================================================

#     @staticmethod
#     def check_service_availability(
#         pincode: str,
#         service_categories: list[str],
#     ):
#         """
#         Complete availability check.

#         Flow:

#         1. Check hub_locations
#         2. Check neatify_service_areas
#         3. Check hub_category_counts
#         4. Check partner assignment
#         """

#         pincode = str(pincode).strip()

#         # -----------------------------------------------------
#         # STEP 1
#         # HUB LOCATION
#         # -----------------------------------------------------

#         hub_location = (
#             CustomerBookingRepository
#             .get_hub_location_by_pincode(
#                 pincode=pincode,
#             )
#         )

#         if not hub_location:
#             return {
#                 "available": False,
#                 "reason": "SERVICE_AREA_NOT_AVAILABLE",
#                 "message": (
#                     "Service is not available "
#                     "in this area."
#                 ),
#                 "pincode": pincode,
#                 "hub": None,
#                 "location": None,
#                 "services": [],
#             }

#         hub_name = (
#             hub_location
#             .get("hub_name")
#         )

#         location_name = (
#             hub_location
#             .get("location_name")
#         )

#         # -----------------------------------------------------
#         # STEP 2
#         # NEATIFY SERVICE AREA
#         #
#         # We check this table as additional coverage
#         # information.
#         #
#         # If your business rule later says this table
#         # should be mandatory, change this to a hard
#         # rejection.
#         # -----------------------------------------------------

#         service_area = (
#             CustomerBookingRepository
#             .get_service_area_by_pincode(
#                 pincode=pincode,
#             )
#         )

#         # -----------------------------------------------------
#         # STEP 3
#         # CHECK EACH SERVICE CATEGORY
#         # -----------------------------------------------------

#         checked_services = []

#         for category in service_categories:

#             if not category:
#                 return {
#                     "available": False,
#                     "reason": "INVALID_SERVICE_CATEGORY",
#                     "message": (
#                         "A selected service has "
#                         "no service category."
#                     ),
#                     "pincode": pincode,
#                     "hub": hub_name,
#                     "location": location_name,
#                     "services": checked_services,
#                 }

#             category = str(category).strip()

#             record = (
#                 CustomerBookingRepository
#                 .get_hub_category_record(
#                     hub_name=hub_name,
#                     category=category,
#                 )
#             )

#             # -------------------------------------------------
#             # CATEGORY DOES NOT EXIST FOR HUB
#             # -------------------------------------------------

#             if not record:
#                 return {
#                     "available": False,
#                     "reason": "SERVICE_NOT_AVAILABLE",
#                     "message": (
#                         f"{category} service is not "
#                         "available in this area."
#                     ),
#                     "pincode": pincode,
#                     "hub": hub_name,
#                     "location": location_name,
#                     "service_area": service_area,
#                     "services": checked_services,
#                 }

#             count = record.get("count") or 0

#             assigned_staff = (
#                 record.get("assigned_staff")
#             )

#             # -------------------------------------------------
#             # NO PARTNER / STAFF
#             # -------------------------------------------------

#             if count <= 0:
#                 return {
#                     "available": False,
#                     "reason": "NO_PARTNER_AVAILABLE",
#                     "message": (
#                         f"No partner is available "
#                         f"for {category} service "
#                         "in this area."
#                     ),
#                     "pincode": pincode,
#                     "hub": hub_name,
#                     "location": location_name,
#                     "service_area": service_area,
#                     "services": checked_services,
#                 }

#             # -------------------------------------------------
#             # CHECK ASSIGNED STAFF
#             # -------------------------------------------------

#             if not assigned_staff:
#                 return {
#                     "available": False,
#                     "reason": "NO_PARTNER_ASSIGNED",
#                     "message": (
#                         f"No partner is currently "
#                         f"assigned for {category} "
#                         "service in this area."
#                     ),
#                     "pincode": pincode,
#                     "hub": hub_name,
#                     "location": location_name,
#                     "service_area": service_area,
#                     "services": checked_services,
#                 }

#             # -------------------------------------------------
#             # SERVICE AVAILABLE
#             # -------------------------------------------------

#             checked_services.append(
#                 {
#                     "category": category,
#                     "count": count,
#                     "assigned_staff": assigned_staff,
#                 }
#             )

#         # -----------------------------------------------------
#         # EVERYTHING AVAILABLE
#         # -----------------------------------------------------

#         return {
#             "available": True,
#             "reason": "AVAILABLE",
#             "message": (
#                 "Services are available "
#                 "in this area."
#             ),
#             "pincode": pincode,
#             "hub": hub_name,
#             "location": location_name,
#             "service_area": service_area,
#             "services": checked_services,
#         }

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
#         add_ons,
#         booking_date: str,
#         booking_time: str,
#         total_amount: float,
#         user_id: str,
#         latitude: float | None = None,
#         longitude: float | None = None,
#         location_link: str | None = None,
#     ):

#         insert_data = {
#             "customer_name": customer_name,

#             "email": email,

#             "phone_number": phone_number,

#             "full_address": full_address,

#             "services": services,

#             "booking_date": booking_date,

#             "booking_time": booking_time,

#             "total_amount": total_amount,

#             "user_id": user_id,

#             "payment_status": "pending",

#             "payment_verified": False,
#         }

#         # =====================================================
#         # ADD-ONS
#         # =====================================================

#         if add_ons:
#             insert_data["add_ons"] = add_ons

#         # =====================================================
#         # LOCATION
#         # =====================================================

#         if latitude is not None:
#             insert_data["latitude"] = latitude

#         if longitude is not None:
#             insert_data["longitude"] = longitude

#         if location_link:
#             insert_data["location_link"] = location_link

#         # =====================================================
#         # INSERT
#         # =====================================================

#         response = (
#             supabase
#             .table("bookings")
#             .insert(insert_data)
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

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
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
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
#                     "razorpay_order_id":
#                         razorpay_order_id,

#                     "payment_status":
#                         "pending",

#                     "payment_verified":
#                         False,
#                 }
#             )
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

#     # =========================================================
#     # GET CUSTOMER BOOKINGS
#     # =========================================================

#     @staticmethod
#     def get_customer_bookings(
#         user_id: str,
#     ):

#         response = (
#             supabase
#             .table("bookings")
#             .select("*")
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .order(
#                 "created_at",
#                 desc=True,
#             )
#             .execute()
#         )

#         return response.data or []

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
#             "razorpay_order_id":
#                 razorpay_order_id,

#             "razorpay_payment_id":
#                 razorpay_payment_id,

#             "razorpay_signature":
#                 razorpay_signature,

#             "payment_status":
#                 "paid",

#             "payment_verified":
#                 True,
#         }

#         if payment_method:
#             update_data[
#                 "payment_method"
#             ] = payment_method

#         response = (
#             supabase
#             .table("bookings")
#             .update(update_data)
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )

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
#                     "payment_status":
#                         "failed",

#                     "payment_verified":
#                         False,
#                 }
#             )
#             .eq(
#                 "id",
#                 booking_id,
#             )
#             .eq(
#                 "user_id",
#                 user_id,
#             )
#             .execute()
#         )

#         return (
#             response.data[0]
#             if response.data
#             else None
#         )














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
                """
                id,
                title,
                price,
                tax_percent,
                service_type
                """
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
                """
                id,
                title,
                price
                """
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
    # FIND SERVICE AREAS BY PINCODE
    # =========================================================

    @staticmethod
    def get_service_areas_by_pincode(
        pincode: str,
    ):
        """
        Find ALL service areas configured for a customer pincode.

        Source:
            neatify_service_areas

        Example:
            500005
                -> CRP Camp
                -> Keshogiri
                -> Mamidipalli
        """

        response = (
            supabase
            .table("neatify_service_areas")
            .select(
                """
                id,
                area_name,
                pincode
                """
            )
            .eq(
                "pincode",
                str(pincode).strip(),
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # FIND HUB LOCATIONS
    # =========================================================

    @staticmethod
    def get_hub_locations(
        hub_name: str | None = None,
        location_name: str | None = None,
    ):
        """
        Find active hub locations.

        This is deliberately NOT used as the first
        pincode availability check.

        neatify_service_areas is checked first.
        """

        query = (
            supabase
            .table("hub_locations")
            .select(
                """
                id,
                hub_name,
                location_name,
                pincode,
                is_active
                """
            )
            .eq(
                "is_active",
                True,
            )
        )

        if hub_name:
            query = query.eq(
                "hub_name",
                hub_name,
            )

        if location_name:
            query = query.ilike(
                "location_name",
                location_name.strip(),
            )

        response = (
            query
            .execute()
        )

        return response.data or []

    # =========================================================
    # FIND ALL HUB LOCATIONS BY PINCODE
    # =========================================================

    @staticmethod
    def get_hub_locations_by_pincode(
        pincode: str,
    ):
        """
        Find all active hub locations mapped to a pincode.

        Source:
            hub_locations

        A pincode may belong to more than one hub,
        so we intentionally return ALL matching rows.
        """

        response = (
            supabase
            .table("hub_locations")
            .select(
                """
                id,
                hub_name,
                location_name,
                pincode,
                is_active
                """
            )
            .eq(
                "pincode",
                str(pincode).strip(),
            )
            .eq(
                "is_active",
                True,
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # GET HUB CATEGORY RECORDS
    # =========================================================

    @staticmethod
    def get_hub_category_records(
        category: str,
    ):
        """
        Get all hub/category mappings for a category.

        Source:
            hub_category_counts

        We intentionally fetch all matching hubs because
        the pincode has already been resolved through
        neatify_service_areas.
        """

        response = (
            supabase
            .table("hub_category_counts")
            .select(
                """
                id,
                hub,
                location,
                category,
                count,
                assigned_staff
                """
            )
            # .eq(
            #     "category",
            #     category,
            # )
            .ilike(
                "category",
                category.strip(),
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # GET HUB CATEGORY RECORD
    # =========================================================

    @staticmethod
    def get_hub_category_record(
        hub_name: str,
        location_name: str,
        category: str,
    ):
        """
        Check whether a category has partners
        in the requested hub AND location.

        Conditions:
            hub matches
            location contains requested location
            category matches
            count > 0
            assigned_staff is not empty
        """

        response = (
            supabase
            .table("hub_category_counts")
            .select(
                """
                id,
                hub,
                location,
                category,
                count,
                assigned_staff
                """
            )
            .eq(
                "hub",
                hub_name,
            )
            .eq(
                "category",
                category,
            )
            .limit(20)
            .execute()
        )

        records = response.data or []

        if not records:
            return None

        requested_location = (
            str(location_name)
            .strip()
            .lower()
        )

        for record in records:

            location_value = (
                str(
                    record.get("location") or ""
                )
                .strip()
                .lower()
            )

            locations = [
                item.strip().lower()
                for item in location_value.split(",")
                if item.strip()
            ]

            if requested_location not in locations:
                continue

            try:
                count = int(
                    record.get("count") or 0
                )
            except (
                ValueError,
                TypeError,
            ):
                count = 0

            assigned_staff = (
                str(
                    record.get(
                        "assigned_staff"
                    ) or ""
                )
                .strip()
            )

            if count > 0 and assigned_staff:
                return record

        return None

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
        booking_date: str,
        booking_time: str,
        total_amount: float,
        user_id: str,
        latitude: float | None = None,
        longitude: float | None = None,
        location_link: str | None = None,
        hub_name: str | None = None,
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
        # HUB
        # =====================================================

        if hub_name:
            insert_data["hub_name"] = hub_name

        # =====================================================
        # LOCATION
        # =====================================================

        if latitude is not None:
            insert_data["latitude"] = latitude

        if longitude is not None:
            insert_data["longitude"] = longitude

        if location_link:
            insert_data["location_link"] = location_link

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
    # GET CUSTOMER BOOKINGS
    # =========================================================

    @staticmethod
    def get_customer_bookings(
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .select("*")
            .eq(
                "user_id",
                user_id,
            )
            .order(
                "created_at",
                desc=True,
            )
            .execute()
        )

        return response.data or []

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