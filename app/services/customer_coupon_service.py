from fastapi import HTTPException, status

from app.repositories.customer_coupon_repository import (
    CustomerCouponRepository,
)


class CustomerCouponService:

    # =========================================================
    # GET AVAILABLE COUPONS
    # =========================================================

    @staticmethod
    def get_available_coupons(
        user_id: str,
        phone_number: str | None = None,
    ):

        coupons = (
            CustomerCouponRepository
            .get_available_coupons(
                user_id=user_id,
                phone_number=phone_number,
            )
        )

        return {
            "success": True,
            "items": coupons,
            "message": (
                "Coupons fetched successfully."
            ),
        }

    # =========================================================
    # VALIDATE COUPON
    # =========================================================

    @staticmethod
    def validate_coupon(
        coupon_code: str,
        user_id: str,
        phone_number: str | None = None,
        service_id: str | None = None,
        subtotal: float = 0,
    ):

        code = coupon_code.strip()

        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon code is required.",
            )

        coupon = (
            CustomerCouponRepository
            .get_coupon_by_code(code)
        )

        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid coupon code.",
            )

        # -----------------------------------------------------
        # ACTIVE CHECK
        # -----------------------------------------------------

        if not coupon.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon is no longer active.",
            )

        # -----------------------------------------------------
        # USED CHECK
        # -----------------------------------------------------

        if coupon.get("is_used"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon has already been used.",
            )

        # -----------------------------------------------------
        # USER CHECK
        # -----------------------------------------------------

        coupon_user_id = coupon.get("user_id")

        if (
            coupon_user_id
            and coupon_user_id != user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon is not valid for this customer.",
            )

        # -----------------------------------------------------
        # PHONE CHECK
        # -----------------------------------------------------

        coupon_phone = coupon.get("phone_number")

        if (
            coupon_phone
            and phone_number
            and coupon_phone != phone_number
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon is not valid for this phone number.",
            )

        # -----------------------------------------------------
        # SERVICE CHECK
        # -----------------------------------------------------

        coupon_service_id = coupon.get("service_id")

        if (
            coupon_service_id
            and service_id
            and coupon_service_id != service_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon is not valid for this service.",
            )

        # -----------------------------------------------------
        # CALCULATE DISCOUNT
        # -----------------------------------------------------

        discount_percentage = float(
            coupon.get("discount_percentage") or 0
        )

        fixed_discount = float(
            coupon.get("discount_amount") or 0
        )

        calculated_discount = 0.0

        if discount_percentage > 0:
            calculated_discount = (
                subtotal * discount_percentage / 100
            )

        elif fixed_discount > 0:
            calculated_discount = fixed_discount

        calculated_discount = min(
            calculated_discount,
            subtotal,
        )

        final_amount = max(
            subtotal - calculated_discount,
            0,
        )

        return {
            "success": True,
            "valid": True,
            "coupon": coupon,
            "discount_amount": calculated_discount,
            "final_amount": final_amount,
            "message": "Coupon applied successfully.",
        }

    # =========================================================
    # MARK COUPON USED
    # =========================================================

    @staticmethod
    def mark_coupon_used(
        coupon_id: str,
        user_id: str,
    ):

        result = (
            CustomerCouponRepository
            .mark_coupon_used(
                coupon_id=coupon_id,
                user_id=user_id,
            )
        )

        return {
            "success": True,
            "items": result,
            "message": "Coupon marked as used.",
        }