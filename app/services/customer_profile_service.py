from fastapi import HTTPException, status

from app.repositories.customer_repository import (
    CustomerRepository,
)


class CustomerProfileService:

    # =========================================================
    # GET PROFILE
    # =========================================================

    @staticmethod
    def get_profile(
        customer,
    ):
        user = customer["user"]
        user_id = str(user.id)

        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        # -----------------------------------------------------
        # PROFILE DOES NOT EXIST
        # -----------------------------------------------------

        if not profile:
            return {
                "id": user_id,
                "full_name": None,
                "email": user.email or "",
                "phone": None,
                "address": None,
                "pincode": None,
            }

        # -----------------------------------------------------
        # AUTH EMAIL IS THE SOURCE OF TRUTH
        # -----------------------------------------------------

        return {
            "id": user_id,
            "full_name": profile.get("full_name"),
            "email": (
                user.email
                or profile.get("email")
                or ""
            ),
            "phone": profile.get("phone"),
            "address": profile.get("address"),
            "pincode": profile.get("pincode"),
        }

    # =========================================================
    # UPDATE PROFILE
    # =========================================================

    @staticmethod
    def update_profile(
        customer,
        full_name: str,
        phone: str,
        address: str,
        pincode: str,
    ):
        user = customer["user"]
        user_id = str(user.id)

        # -----------------------------------------------------
        # CLEAN PHONE
        # -----------------------------------------------------

        clean_phone = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Phone number must be exactly "
                    "10 digits."
                ),
            )

        # -----------------------------------------------------
        # CLEAN DATA
        # -----------------------------------------------------

        clean_name = full_name.strip()
        clean_address = address.strip()
        clean_pincode = pincode.strip()

        if not clean_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name is required.",
            )

        # -----------------------------------------------------
        # AUTH EMAIL
        # -----------------------------------------------------

        email = user.email or ""

        # -----------------------------------------------------
        # UPSERT PROFILE
        # -----------------------------------------------------

        CustomerRepository.upsert_profile(
            user_id=user_id,
            full_name=clean_name,
            phone=clean_phone,
            address=clean_address,
            pincode=clean_pincode,
            email=email,
        )

        # -----------------------------------------------------
        # RETURN UPDATED PROFILE
        # -----------------------------------------------------

        return (
            CustomerProfileService
            .get_profile(
                customer=customer,
            )
        )