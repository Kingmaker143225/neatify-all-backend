from app.supabase.client import supabase


class CustomerCouponRepository:

    # =========================================================
    # GET AVAILABLE COUPONS
    # =========================================================

    @staticmethod
    def get_available_coupons(
        user_id: str | None = None,
        phone_number: str | None = None,
    ):
        query = (
            supabase
            .table("coupons")
            .select(
                """
                id,
                coupon_code,
                discount_percentage,
                phone_number,
                is_used,
                created_at,
                discount_amount,
                is_active,
                service_id,
                user_id
                """
            )
            .eq("is_active", True)
            .eq("is_used", False)
        )

        response = query.execute()

        coupons = response.data or []

        # -----------------------------------------------------
        # Filter coupons belonging to this customer
        # -----------------------------------------------------

        if user_id or phone_number:
            filtered = []

            for coupon in coupons:

                coupon_user_id = coupon.get("user_id")
                coupon_phone = coupon.get("phone_number")

                # Global coupon
                if not coupon_user_id and not coupon_phone:
                    filtered.append(coupon)
                    continue

                # User-specific coupon
                if user_id and coupon_user_id == user_id:
                    filtered.append(coupon)
                    continue

                # Phone-specific coupon
                if phone_number and coupon_phone == phone_number:
                    filtered.append(coupon)
                    continue

            coupons = filtered

        return coupons

    # =========================================================
    # GET COUPON BY CODE
    # =========================================================

    @staticmethod
    def get_coupon_by_code(
        coupon_code: str,
    ):
        response = (
            supabase
            .table("coupons")
            .select(
                """
                id,
                coupon_code,
                discount_percentage,
                phone_number,
                is_used,
                created_at,
                discount_amount,
                is_active,
                service_id,
                user_id
                """
            )
            .eq(
                "coupon_code",
                coupon_code,
            )
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # MARK COUPON AS USED
    # =========================================================

    @staticmethod
    def mark_coupon_used(
        coupon_id: str,
        user_id: str,
    ):
        response = (
            supabase
            .table("coupons")
            .update(
                {
                    "is_used": True,
                    "user_id": user_id,
                }
            )
            .eq("id", coupon_id)
            .execute()
        )

        return response.data