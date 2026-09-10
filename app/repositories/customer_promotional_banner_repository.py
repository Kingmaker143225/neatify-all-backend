# from datetime import datetime, timezone

# from app.supabase.client import supabase


# class CustomerPromotionalBannerRepository:

#     @staticmethod
#     def get_active_banners():
#         now = datetime.now(timezone.utc).isoformat()

#         # ---------------------------------------------------------
#         # GET ACTIVE BANNERS
#         # ---------------------------------------------------------
#         banner_response = (
#             supabase
#             .table("promotional_banners")
#             .select(
#                 """
#                 id,
#                 image_url,
#                 is_active,
#                 display_order,
#                 start_date,
#                 end_date,
#                 storage_path,
#                 customer_type,
#                 booking_condition,
#                 location_scope,
#                 service_scope,
#                 pincode_scope,
#                 offer_percentage
#                 """
#             )
#             .eq("is_active", True)
#             .order("display_order", desc=False)
#             .execute()
#         )

#         banners = banner_response.data or []

#         # ---------------------------------------------------------
#         # DATE FILTER
#         # ---------------------------------------------------------
#         filtered_banners = []

#         for banner in banners:
#             start_date = banner.get("start_date")
#             end_date = banner.get("end_date")

#             if start_date and start_date > now:
#                 continue

#             if end_date and end_date < now:
#                 continue

#             filtered_banners.append(banner)

#         # ---------------------------------------------------------
#         # LOAD SERVICES + LOCATIONS FOR EACH BANNER
#         # ---------------------------------------------------------
#         for banner in filtered_banners:

#             banner_id = banner["id"]

#             # -----------------------------------------------------
#             # SERVICES
#             # -----------------------------------------------------
#             service_response = (
#                 supabase
#                 .table("promotional_banner_services")
#                 .select(
#                     """
#                     service_id,
#                     services (
#                         id,
#                         title,
#                         slug,
#                         service_type
#                     )
#                     """
#                 )
#                 .eq("banner_id", banner_id)
#                 .execute()
#             )

#             service_rows = service_response.data or []

#             banner["services"] = [
#                 row["services"]
#                 for row in service_rows
#                 if row.get("services")
#             ]

#             banner["service_ids"] = [
#                 row["service_id"]
#                 for row in service_rows
#             ]

#             # -----------------------------------------------------
#             # LOCATIONS
#             # -----------------------------------------------------
#             location_response = (
#                 supabase
#                 .table("promotional_banner_locations")
#                 .select(
#                     """
#                     location_id,
#                     hub_locations (
#                         id,
#                         hub_name,
#                         location_name,
#                         pincode
#                     )
#                     """
#                 )
#                 .eq("banner_id", banner_id)
#                 .execute()
#             )

#             location_rows = location_response.data or []

#             banner["locations"] = [
#                 row["hub_locations"]
#                 for row in location_rows
#                 if row.get("hub_locations")
#             ]

#             banner["location_ids"] = [
#                 row["location_id"]
#                 for row in location_rows
#             ]

#         return filtered_banners
















from datetime import datetime, timezone

from app.supabase.client import supabase


class CustomerPromotionalBannerRepository:

    # =========================================================
    # GET ACTIVE PROMOTIONAL BANNERS
    # =========================================================

    @staticmethod
    def get_active_banners(
        user_id: str,
        pincode: str | None = None,
    ):
        # -----------------------------------------------------
        # 1. FETCH ACTIVE BANNERS
        # -----------------------------------------------------

        response = (
            supabase
            .table("promotional_banners")
            .select(
                """
                id,
                image_url,
                is_active,
                display_order,
                start_date,
                end_date,
                created_at,
                updated_at,
                storage_path,
                customer_type,
                booking_condition,
                location_scope,
                service_scope,
                pincode_scope,
                offer_percentage
                """
            )
            .eq(
                "is_active",
                True,
            )
            .order(
                "display_order",
                desc=False,
            )
            .execute()
        )

        banners = response.data or []

        if not banners:
            return []

        # -----------------------------------------------------
        # 2. CURRENT TIME
        # -----------------------------------------------------

        now = datetime.now(timezone.utc)

        # -----------------------------------------------------
        # 3. GET CUSTOMER BOOKING COUNT
        # -----------------------------------------------------

        booking_response = (
            supabase
            .table("bookings")
            .select(
                "id",
                count="exact",
                head=True,
            )
            .eq(
                "user_id",
                user_id,
            )
            .execute()
        )

        booking_count = booking_response.count or 0

        # -----------------------------------------------------
        # 4. DETERMINE CUSTOMER TYPE
        # -----------------------------------------------------

        is_new_customer = booking_count == 0
        is_existing_customer = booking_count > 0

        # -----------------------------------------------------
        # 5. RESOLVE CUSTOMER HUB LOCATIONS
        # -----------------------------------------------------

        customer_hub_ids: list[str] = []

        clean_pincode = (
            pincode.strip()
            if pincode
            else None
        )

        if clean_pincode:

            hub_response = (
                supabase
                .table("hub_locations")
                .select("id")
                .eq(
                    "pincode",
                    clean_pincode,
                )
                .eq(
                    "is_active",
                    True,
                )
                .execute()
            )

            hub_data = hub_response.data or []

            customer_hub_ids = [
                str(item["id"])
                for item in hub_data
                if item.get("id")
            ]

        # -----------------------------------------------------
        # 6. FETCH BANNER LOCATION RELATIONSHIPS
        # -----------------------------------------------------

        location_response = (
            supabase
            .table("promotional_banner_locations")
            .select(
                "banner_id, location_id"
            )
            .execute()
        )

        banner_locations = (
            location_response.data or []
        )

        banner_location_map: dict[str, list[str]] = {}

        for item in banner_locations:

            banner_id = item.get("banner_id")
            location_id = item.get("location_id")

            if not banner_id or not location_id:
                continue

            banner_id = str(banner_id)
            location_id = str(location_id)

            if banner_id not in banner_location_map:
                banner_location_map[banner_id] = []

            banner_location_map[banner_id].append(
                location_id
            )

        # -----------------------------------------------------
        # 7. FETCH BANNER SERVICE RELATIONSHIPS
        # -----------------------------------------------------

        service_response = (
            supabase
            .table("promotional_banner_services")
            .select(
                "banner_id, service_id"
            )
            .execute()
        )

        banner_services = (
            service_response.data or []
        )

        banner_service_map: dict[str, list[str]] = {}

        for item in banner_services:

            banner_id = item.get("banner_id")
            service_id = item.get("service_id")

            if not banner_id or not service_id:
                continue

            banner_id = str(banner_id)
            service_id = str(service_id)

            if banner_id not in banner_service_map:
                banner_service_map[banner_id] = []

            banner_service_map[banner_id].append(
                service_id
            )

        # -----------------------------------------------------
        # 8. COLLECT ALL SERVICE IDS
        # -----------------------------------------------------

        all_service_ids: list[str] = []

        for service_ids in banner_service_map.values():

            for service_id in service_ids:

                if service_id not in all_service_ids:
                    all_service_ids.append(service_id)

        # -----------------------------------------------------
        # 9. FETCH SERVICE DETAILS
        # -----------------------------------------------------

        service_map: dict[str, dict] = {}

        if all_service_ids:

            services_response = (
                supabase
                .table("services")
                .select(
                    "id, title"
                )
                .in_(
                    "id",
                    all_service_ids,
                )
                .execute()
            )

            services_data = (
                services_response.data or []
            )

            for service in services_data:

                service_id = service.get("id")

                if service_id:
                    service_map[str(service_id)] = {
                        "id": str(service_id),
                        "title": service.get("title"),
                    }

        # -----------------------------------------------------
        # 10. FILTER BANNERS
        # -----------------------------------------------------

        eligible_banners = []

        for banner in banners:

            banner_id = str(
                banner.get("id")
            )

            # -------------------------------------------------
            # DATE CHECK
            # -------------------------------------------------

            start_date = banner.get(
                "start_date"
            )

            end_date = banner.get(
                "end_date"
            )

            if start_date:

                if isinstance(start_date, str):

                    try:
                        start_date = (
                            datetime.fromisoformat(
                                start_date.replace(
                                    "Z",
                                    "+00:00",
                                )
                            )
                        )
                    except ValueError:
                        start_date = None

                if (
                    start_date
                    and start_date.tzinfo is None
                ):
                    start_date = start_date.replace(
                        tzinfo=timezone.utc
                    )

                if (
                    start_date
                    and now < start_date
                ):
                    continue

            if end_date:

                if isinstance(end_date, str):

                    try:
                        end_date = (
                            datetime.fromisoformat(
                                end_date.replace(
                                    "Z",
                                    "+00:00",
                                )
                            )
                        )
                    except ValueError:
                        end_date = None

                if (
                    end_date
                    and end_date.tzinfo is None
                ):
                    end_date = end_date.replace(
                        tzinfo=timezone.utc
                    )

                if (
                    end_date
                    and now > end_date
                ):
                    continue

            # -------------------------------------------------
            # CUSTOMER TYPE CHECK
            # -------------------------------------------------

            customer_type = (
                banner.get("customer_type")
                or "everyone"
            )

            customer_type = (
                str(customer_type)
                .strip()
                .lower()
            )

            customer_eligible = False

            if customer_type == "everyone":

                customer_eligible = True

            elif customer_type == "new":

                customer_eligible = (
                    is_new_customer
                )

            elif customer_type == "existing":

                customer_eligible = (
                    is_existing_customer
                )

            else:

                # Unknown customer type:
                # do not expose the banner.
                customer_eligible = False

            if not customer_eligible:
                continue

            # -------------------------------------------------
            # LOCATION CHECK
            # -------------------------------------------------

            pincode_scope = (
                banner.get("pincode_scope")
                or "all"
            )

            pincode_scope = (
                str(pincode_scope)
                .strip()
                .lower()
            )

            location_eligible = False

            if pincode_scope == "all":

                location_eligible = True

            elif pincode_scope == "selected":

                allowed_location_ids = (
                    banner_location_map.get(
                        banner_id,
                        [],
                    )
                )

                location_eligible = any(
                    hub_id in allowed_location_ids
                    for hub_id in customer_hub_ids
                )

            else:

                # Unknown scope:
                # don't expose banner.
                location_eligible = False

            if not location_eligible:
                continue

            # -------------------------------------------------
            # SERVICE DETAILS
            # -------------------------------------------------

            service_ids = (
                banner_service_map.get(
                    banner_id,
                    [],
                )
            )

            services = []

            for service_id in service_ids:

                service = service_map.get(
                    service_id
                )

                if service:
                    services.append(service)

            # -------------------------------------------------
            # LOCATION IDS
            # -------------------------------------------------

            location_ids = (
                banner_location_map.get(
                    banner_id,
                    [],
                )
            )

            # -------------------------------------------------
            # FINAL RESPONSE OBJECT
            # -------------------------------------------------

            banner["service_ids"] = service_ids

            banner["services"] = services

            banner["location_ids"] = location_ids

            banner["customer_booking_count"] = (
                booking_count
            )

            banner["customer_pincode"] = (
                clean_pincode
            )

            banner["customer_hub_ids"] = (
                customer_hub_ids
            )

            eligible_banners.append(
                banner
            )

        return eligible_banners