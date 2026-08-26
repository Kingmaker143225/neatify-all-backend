from app.supabase.client import supabase


class PartnerEarningsRepository:
    
    @staticmethod
    def get_pending_payments(
        staff_email: str,
    ):
        # =====================================================
        # GET COMPLETED BOOKINGS FOR PARTNER
        # =====================================================

        bookings_response = (
            supabase
            .table("bookings")
            .select(
                "id,customer_name,staff_earned_amount,work_ended_at"
            )
            .eq(
                "assigned_staff_email",
                staff_email,
            )
            .eq(
                "work_status",
                "COMPLETED",
            )
            .order(
                "work_ended_at",
                desc=True,
            )
            .execute()
        )

        completed_bookings = (
            bookings_response.data or []
        )

        if not completed_bookings:
            return []

        # =====================================================
        # GET BOOKING IDS
        # =====================================================

        booking_ids = [
            booking.get("id")
            for booking in completed_bookings
            if booking.get("id")
        ]

        if not booking_ids:
            return []

        # =====================================================
        # GET PAYMENT STATUS
        # =====================================================

        earnings_response = (
            supabase
            .table("staff_earnings")
            .select(
                "booking_id,payment_status"
            )
            .in_(
                "booking_id",
                booking_ids,
            )
            .execute()
        )

        earnings_data = (
            earnings_response.data or []
        )

        # =====================================================
        # CREATE PAYMENT STATUS MAP
        # =====================================================

        payment_map = {}

        for item in earnings_data:
            booking_id = item.get("booking_id")

            if booking_id:
                payment_map[str(booking_id)] = (
                    item.get("payment_status")
                    or "pending"
                )

        # =====================================================
        # BUILD PENDING LIST
        # =====================================================

        pending_bookings = []

        for booking in completed_bookings:

            booking_id = booking.get("id")

            if not booking_id:
                continue

            payment_status = payment_map.get(
                str(booking_id),
                "pending",
            )

            # Ignore already paid bookings
            if (
                str(payment_status).lower()
                == "paid"
            ):
                continue

            pending_bookings.append(
                {
                    "id": str(booking_id),
                    "customer_name":
                        booking.get(
                            "customer_name"
                        )
                        or "Customer",
                    "amount": float(
                        booking.get(
                            "staff_earned_amount"
                        )
                        or 0
                    ),
                    "earned_at":
                        booking.get(
                            "work_ended_at"
                        ),
                    "payment_status":
                        payment_status,
                }
            )

        return pending_bookings

    @staticmethod
    def get_paid_earnings(
        staff_email: str,
        start_date: str,
        end_date: str,
    ):
        response = (
            supabase
            .table("staff_earnings")
            .select(
                "id,Customer_Name,AMOUNT,earned_at"
            )
            .eq("staff_email", staff_email)
            .eq("payment_status", "paid")
            .gte("earned_at", start_date)
            .lte("earned_at", end_date)
            .order("earned_at", desc=False)
            .execute()
        )

        return response.data or []


    @staticmethod
    def get_total_earnings(staff_email: str):
        response = (
            supabase
            .table("staff_earnings")
            .select(
                "id,Customer_Name,AMOUNT,earned_at"
            )
            .eq("staff_email", staff_email)
            .eq("payment_status", "paid")
            .order("earned_at", desc=True)
            .execute()
        )

        return response.data or []