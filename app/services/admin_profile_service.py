from fastapi import HTTPException

from app.repositories.admin_profile_repository import (
    AdminProfileRepository,
)


class AdminProfileService:

    # =========================================================
    # GET PROFILE
    # =========================================================

    @staticmethod
    def get_profile(
        admin,
    ):

        user = admin["user"]

        user_id = str(
            user.id
        )

        result = (
            AdminProfileRepository
            .get_profile(
                user_id=user_id,
            )
        )

        signup = (
            result.get("signup")
            or {}
        )

        profile = (
            result.get("profile")
            or {}
        )

        # -----------------------------------------------------
        # AUTH EMAIL
        #
        # Supabase Auth email is preferred.
        # -----------------------------------------------------

        email = (
            user.email
            or signup.get("email")
            or profile.get("email")
            or ""
        )

        # -----------------------------------------------------
        # MERGE DATA
        #
        # Same fallback logic your old frontend used.
        # -----------------------------------------------------

        return {
            "id": user_id,

            "full_name": (
                profile.get("full_name")
                or signup.get("full_name")
                or ""
            ),

            "email": email,

            "phone": (
                profile.get("phone")
                or signup.get("phone")
                or ""
            ),

            "address": (
                profile.get("address")
                or ""
            ),

            "pincode": (
                profile.get("pincode")
                or ""
            ),
        }

    # =========================================================
    # UPDATE PROFILE
    # =========================================================

    @staticmethod
    def update_profile(
        admin,
        full_name: str,
        phone: str,
        address: str,
        pincode: str,
    ):

        user = admin["user"]

        user_id = str(
            user.id
        )

        # -----------------------------------------------------
        # VALIDATE PHONE
        # -----------------------------------------------------

        clean_phone = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Phone number must be exactly "
                    "10 digits."
                ),
            )

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        AdminProfileRepository.update_profile(
            user_id=user_id,
            full_name=full_name.strip(),
            phone=clean_phone,
            address=address.strip(),
            pincode=pincode.strip(),
        )

        # -----------------------------------------------------
        # RETURN UPDATED PROFILE
        # -----------------------------------------------------

        return (
            AdminProfileService
            .get_profile(
                admin=admin,
            )
        )