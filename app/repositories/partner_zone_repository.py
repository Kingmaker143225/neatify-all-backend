# from app.supabase.client import supabase


# class PartnerZoneRepository:

#     # =========================================================
#     # GET PARTNER ZONE
#     # =========================================================

#     @staticmethod
#     def get_partner_zone(email: str):
#         # -----------------------------------------------------
#         # 1. Find partner's assigned hub
#         # -----------------------------------------------------

#         hubs_response = (
#             supabase
#             .from_("hub_category_counts")
#             .select("hub, location, assigned_staff")
#             .execute()
#         )

#         hubs = hubs_response.data or []

#         email_normalized = email.lower().strip()

#         match = None

#         for item in hubs:
#             assigned_staff = str(
#                 item.get("assigned_staff") or ""
#             ).lower()

#             if email_normalized in assigned_staff:
#                 match = item
#                 break

#         if not match:
#             return None

#         hub_name = (
#             str(match.get("hub") or "Assigned Zone")
#             .strip()
#         )

#         # -----------------------------------------------------
#         # 2. Get hub locations
#         # -----------------------------------------------------

#         locations_response = (
#             supabase
#             .from_("hub_locations")
#             .select("location_name, pincode")
#             .eq("hub_name", hub_name)
#             .execute()
#         )

#         locations = locations_response.data or []

#         sub_locations = [
#             {
#                 "location_name": str(
#                     row.get("location_name") or ""
#                 ).strip(),
#                 "pincode": str(
#                     row.get("pincode") or ""
#                 ).strip(),
#             }
#             for row in locations
#         ]

#         # -----------------------------------------------------
#         # 3. Get current partner location/status
#         # -----------------------------------------------------

#         profile_response = (
#             supabase
#             .from_("staff_profile")
#             .select(
#                 "live_location, is_out_of_zone"
#             )
#             .eq("email", email)
#             .maybe_single()
#             .execute()
#         )

#         profile = profile_response.data or {}

#         return {
#             "hub_name": hub_name,
#             "location": match.get("location") or "",
#             "sub_locations": sub_locations,
#             "live_location": profile.get(
#                 "live_location"
#             ),
#             "is_out_of_zone": bool(
#                 profile.get("is_out_of_zone", False)
#             ),
#         }

#     # =========================================================
#     # UPDATE PARTNER LOCATION / ZONE STATUS
#     # =========================================================

#     @staticmethod
#     def update_location(
#         email: str,
#         live_location: str | None = None,
#         is_out_of_zone: bool | None = None,
#     ):
#         update_data = {}

#         if live_location is not None:
#             update_data["live_location"] = live_location

#         if is_out_of_zone is not None:
#             update_data["is_out_of_zone"] = is_out_of_zone

#         if not update_data:
#             return True

#         (
#             supabase
#             .from_("staff_profile")
#             .update(update_data)
#             .eq("email", email)
#             .execute()
#         )

#         return True



















from app.supabase.client import supabase


class PartnerZoneRepository:

    # =========================================================
    # GET PARTNER ZONE
    # =========================================================

    @staticmethod
    def get_partner_zone(email: str):

        # -----------------------------------------------------
        # 1. Find partner's assigned hub
        # -----------------------------------------------------

        hubs_response = (
            supabase
            .from_("hub_category_counts")
            .select(
                "hub, location, assigned_staff"
            )
            .execute()
        )

        hubs = hubs_response.data or []

        email_normalized = (
            email.lower().strip()
        )

        match = None

        for item in hubs:

            assigned_staff = str(
                item.get("assigned_staff") or ""
            ).lower()

            if email_normalized in assigned_staff:
                match = item
                break

        # -----------------------------------------------------
        # No assigned hub found
        # -----------------------------------------------------

        if not match:
            return None

        # -----------------------------------------------------
        # Hub name
        # -----------------------------------------------------

        hub_name = (
            str(
                match.get("hub")
                or "Assigned Zone"
            )
            .strip()
        )

        # -----------------------------------------------------
        # 2. Get assigned hub locations
        #
        # IMPORTANT:
        # We only get location_name + pincode.
        #
        # No latitude/longitude are stored in the database.
        # The mobile app will geocode these values.
        # -----------------------------------------------------

        locations_response = (
            supabase
            .from_("hub_locations")
            .select(
                "location_name, pincode"
            )
            .eq(
                "hub_name",
                hub_name
            )
            .execute()
        )

        locations = (
            locations_response.data or []
        )

        # -----------------------------------------------------
        # Build sub-location response
        # -----------------------------------------------------

        sub_locations = []

        for row in locations:

            location_name = str(
                row.get(
                    "location_name"
                ) or ""
            ).strip()

            pincode = str(
                row.get(
                    "pincode"
                ) or ""
            ).strip()

            sub_locations.append(
                {
                    "location_name": location_name,
                    "pincode": pincode,
                }
            )

        # -----------------------------------------------------
        # 3. Get current partner location/status
        # -----------------------------------------------------

        profile_response = (
            supabase
            .from_("staff_profile")
            .select(
                "live_location, is_out_of_zone"
            )
            .eq(
                "email",
                email
            )
            .maybe_single()
            .execute()
        )

        profile = (
            profile_response.data or {}
        )

        # -----------------------------------------------------
        # 4. Return assigned zone
        # -----------------------------------------------------

        return {
            "hub_name": hub_name,

            "location": (
                match.get("location")
                or ""
            ),

            "sub_locations": sub_locations,

            "live_location": (
                profile.get(
                    "live_location"
                )
            ),

            "is_out_of_zone": bool(
                profile.get(
                    "is_out_of_zone",
                    False
                )
            ),
        }

    # =========================================================
    # UPDATE PARTNER LOCATION / ZONE STATUS
    # =========================================================

    @staticmethod
    def update_location(
        email: str,
        live_location: str | None = None,
        is_out_of_zone: bool | None = None,
    ):

        update_data = {}

        # -----------------------------------------------------
        # Live location
        # -----------------------------------------------------

        if live_location is not None:

            update_data[
                "live_location"
            ] = live_location

        # -----------------------------------------------------
        # Zone status
        # -----------------------------------------------------

        if is_out_of_zone is not None:

            update_data[
                "is_out_of_zone"
            ] = is_out_of_zone

        # -----------------------------------------------------
        # Nothing to update
        # -----------------------------------------------------

        if not update_data:
            return True

        # -----------------------------------------------------
        # Update staff profile
        # -----------------------------------------------------

        (
            supabase
            .from_("staff_profile")
            .update(
                update_data
            )
            .eq(
                "email",
                email
            )
            .execute()
        )

        return True