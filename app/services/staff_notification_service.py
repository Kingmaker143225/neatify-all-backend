from fastapi import HTTPException

from app.supabase.admin_client import supabase_admin
from app.services.notification_service import NotificationService


class StaffNotificationService:

    @staticmethod
    async def send_staff_notification(
        email: str,
        title: str | None = None,
        body: str | None = None,
    ):

        # =====================================================
        # DEFAULT VALUES
        # =====================================================

        notification_title = (
            title or "New Service Assigned"
        )

        notification_body = (
            body or "You have a new service"
        )

        # =====================================================
        # FETCH STAFF PUSH TOKEN
        # =====================================================

        response = (
            supabase_admin
            .table("staff_profile")
            .select("push_token")
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        staff = response.data

        if not staff:
            raise HTTPException(
                status_code=404,
                detail="Staff profile not found.",
            )

        push_token = staff.get("push_token")

        if not push_token:
            raise HTTPException(
                status_code=400,
                detail="No push token found.",
            )

        print(
            "✅ Sending staff notification to:",
            email,
        )

        # =====================================================
        # SEND EXPO PUSH
        # =====================================================

        notification_result = (
            await NotificationService.send_to_token(
                token=push_token,
                title=notification_title,
                body=notification_body,
                data={
                    "screen": "pending-services",
                },
            )
        )

        print(
            "📩 Expo notification result:",
            notification_result,
        )

        # =====================================================
        # FETCH LATEST BOOKING
        # =====================================================

        booking_response = (
            supabase_admin
            .table("bookings")
            .select("*")
            .eq(
                "assigned_staff_email",
                email,
            )
            .order(
                "created_at",
                desc=True,
            )
            .limit(1)
            .execute()
        )

        booking_data = (
            booking_response.data
            or []
        )

        booking = (
            booking_data[0]
            if booking_data
            else None
        )

        # =====================================================
        # STORE NOTIFICATION
        # =====================================================

        notification_data = {
            "staff_email": email,
            "title": notification_title,
            "body": notification_body,
            "type": "new_service",
            "is_read": False,
            "booking_id": (
                booking.get("id")
                if booking
                else None
            ),
            "customer_name": (
                booking.get("customer_name")
                if booking
                else None
            ),
            "booking_time": (
                booking.get("booking_time")
                if booking
                else None
            ),
            "booking_date": (
                booking.get("booking_date")
                if booking
                else None
            ),
            "services": (
                booking.get("services")
                if booking
                else None
            ),
            "full_address": (
                booking.get("full_address")
                if booking
                else None
            ),
            "phone_number": (
                booking.get("phone_number")
                if booking
                else None
            ),
        }

        notification_response = (
            supabase_admin
            .table("notifications")
            .insert(notification_data)
            .execute()
        )

        print(
            "✅ Notification stored in DB"
        )

        # =====================================================
        # RETURN
        # =====================================================

        return {
            "success": True,
            "message": "Staff notification sent successfully.",
            "email": email,
            "push_token_found": True,
            "notification": notification_result,
            "booking": booking,
            "stored_notification": (
                notification_response.data
            ),
        }