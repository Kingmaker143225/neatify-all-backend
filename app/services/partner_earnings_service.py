from datetime import date, datetime, timedelta

from app.repositories.partner_earnings_repository import (
    PartnerEarningsRepository,
)


class PartnerEarningsService:

    @staticmethod
    def get_weekly_earnings(
        staff_email: str,
        year: int,
        month: int,
        week: int,
    ):

        # First day of selected month
        first_day = date(year, month, 1)

        # Sunday-based calendar start
        calendar_start = (
            first_day
            - timedelta(days=(first_day.weekday() + 1) % 7)
        )

        # Selected week start
        start_date = (
            calendar_start
            + timedelta(days=(week - 1) * 7)
        )

        # Selected week end
        end_date = start_date + timedelta(days=6)

        # Query range
        query_start = datetime.combine(
            start_date,
            datetime.min.time(),
        ).isoformat()

        query_end = datetime.combine(
            end_date,
            datetime.max.time(),
        ).isoformat()

        records = (
            PartnerEarningsRepository.get_paid_earnings(
                staff_email=staff_email,
                start_date=query_start,
                end_date=query_end,
            )
        )

        # =====================================================
        # DAILY EARNINGS
        # =====================================================

        daily_map = {}

        for i in range(7):
            current_date = (
                start_date
                + timedelta(days=i)
            )

            daily_map[
                current_date.isoformat()
            ] = 0

        bookings = []

        for item in records:

            earned_at = item.get("earned_at")

            if not earned_at:
                continue

            try:
                earned_datetime = (
                    datetime.fromisoformat(
                        earned_at.replace(
                            "Z",
                            "+00:00",
                        )
                    )
                )

                earned_date = (
                    earned_datetime.date()
                )

            except Exception:
                continue

            date_key = earned_date.isoformat()

            amount = float(
                item.get("AMOUNT") or 0
            )

            if date_key in daily_map:
                daily_map[date_key] += amount

            bookings.append(
                {
                    "id": str(
                        item.get("id")
                    ),
                    "customer_name":
                        item.get(
                            "Customer_Name"
                        )
                        or "Customer",
                    "amount": amount,
                    "earned_at":
                        earned_at,
                }
            )

        # =====================================================
        # DAILY RESPONSE
        # =====================================================

        daily = [
            {
                "date": date_key,
                "amount": amount,
            }
            for date_key, amount
            in daily_map.items()
        ]

        # =====================================================
        # TOTAL
        # =====================================================

        total_earnings = sum(
            item["amount"]
            for item in daily
        )

        return {
            "year": year,
            "month": f"{month:02d}",
            "week": week,
            "start_date":
                start_date.isoformat(),
            "end_date":
                end_date.isoformat(),
            "earnings":
                total_earnings,
            "daily": daily,
            "bookings": bookings,
        }
    
    @staticmethod
    def get_pending_payments(
        staff_email: str,
    ):

        records = (
            PartnerEarningsRepository
            .get_pending_payments(
                staff_email=staff_email,
            )
        )

        total_pending = 0

        bookings = []

        for item in records:

            amount = float(
                item.get("amount") or 0
            )

            total_pending += amount

            bookings.append(
                {
                    "id": str(
                        item.get("id")
                    ),
                    "customer_name":
                        item.get(
                            "customer_name"
                        )
                        or "Customer",
                    "amount": amount,
                    "earned_at":
                        item.get("earned_at"),
                    "payment_status":
                        item.get(
                            "payment_status"
                        )
                        or "pending",
                }
            )

        return {
            "total_pending": total_pending,
            "count": len(bookings),
            "bookings": bookings,
        }

    @staticmethod
    def get_total_earnings(staff_email: str):

        records = (
            PartnerEarningsRepository
            .get_total_earnings(staff_email)
        )

        bookings = []

        total_earnings = 0

        for item in records:

            amount = float(
                item.get("AMOUNT") or 0
            )

            total_earnings += amount

            bookings.append(
                {
                    "id": str(
                        item.get("id")
                    ),
                    "customer_name":
                        item.get(
                            "Customer_Name"
                        )
                        or "Customer",
                    "amount": amount,
                    "earned_at":
                        item.get("earned_at"),
                }
            )

        return {
            "total_earnings":
                total_earnings,
            "count":
                len(bookings),
            "bookings":
                bookings,
        }
    @staticmethod
    def get_monthly_earnings(
        staff_email: str,
        year: int,
        month: int,
    ):

        # =====================================================
        # MONTH START / END
        # =====================================================

        first_day = date(year, month, 1)

        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)

        last_day = next_month - timedelta(days=1)

        # =====================================================
        # QUERY RANGE
        # =====================================================

        query_start = datetime.combine(
            first_day,
            datetime.min.time(),
        ).isoformat()

        query_end = datetime.combine(
            last_day,
            datetime.max.time(),
        ).isoformat()

        # =====================================================
        # FETCH PAID EARNINGS
        # =====================================================

        records = (
            PartnerEarningsRepository.get_paid_earnings(
                staff_email=staff_email,
                start_date=query_start,
                end_date=query_end,
            )
        )

        # =====================================================
        # BOOKINGS
        # =====================================================

        bookings = []

        total_earnings = 0

        for item in records:

            amount = float(
                item.get("AMOUNT") or 0
            )

            total_earnings += amount

            bookings.append(
                {
                    "id": str(
                        item.get("id")
                    ),
                    "customer_name":
                        item.get(
                            "Customer_Name"
                        )
                        or "Customer",
                    "amount": amount,
                    "earned_at":
                        item.get("earned_at"),
                }
            )

        # =====================================================
        # RESPONSE
        # =====================================================

        return {
            "year": year,
            "month": f"{month:02d}",
            "earnings": total_earnings,
            "bookings": bookings,
        }