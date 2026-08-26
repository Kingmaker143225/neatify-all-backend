from datetime import datetime, timezone

import httpx

from app.repositories.booking_reminder_repository import (
    BookingReminderRepository,
)


EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


class BookingReminderService:

    @staticmethod
    async def process_reminders():

        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()

        print("🚀 BOOKING REMINDER JOB STARTED")
        print("⌚ CURRENT UTC:", now_iso)

        bookings = (
            BookingReminderRepository
            .get_future_bookings(now_iso)
        )

        print(
            "📦 FUTURE BOOKINGS FOUND:",
            len(bookings),
        )

        processed = 0
        sent = 0
        skipped = 0
        errors = 0

        async with httpx.AsyncClient(timeout=20) as client:

            for booking in bookings:

                try:
                    processed += 1

                    booking_schedule_at = (
                        booking.get("booking_schedule_at")
                    )

                    assigned_staff_email = (
                        booking.get("assigned_staff_email")
                    )

                    if (
                        not booking_schedule_at
                        or not assigned_staff_email
                    ):
                        skipped += 1
                        continue

                    # -------------------------------------------------
                    # BOOKING TIME
                    # -------------------------------------------------

                    booking_time = (
                        datetime.fromisoformat(
                            booking_schedule_at.replace(
                                "Z",
                                "+00:00",
                            )
                        )
                    )

                    if booking_time.tzinfo is None:
                        booking_time = booking_time.replace(
                            tzinfo=timezone.utc
                        )

                    # -------------------------------------------------
                    # TIME DIFFERENCE
                    # -------------------------------------------------

                    diff_seconds = (
                        booking_time - now
                    ).total_seconds()

                    diff_minutes = int(
                        diff_seconds // 60
                    )

                    print(
                        f"👤 {booking.get('customer_name')} | "
                        f"BOOKING UTC: {booking_schedule_at} | "
                        f"DIFF: {diff_minutes}"
                    )

                    # -------------------------------------------------
                    # STAFF
                    # -------------------------------------------------

                    staff = (
                        BookingReminderRepository
                        .get_staff_by_email(
                            assigned_staff_email
                        )
                    )

                    if not staff:
                        print(
                            f"❌ Staff not found: "
                            f"{assigned_staff_email}"
                        )
                        skipped += 1
                        continue

                    push_token = staff.get("push_token")
                    staff_name = (
                        staff.get("name")
                        or "Staff"
                    )

                    if not push_token:
                        print(
                            f"❌ No push token found for "
                            f"{assigned_staff_email}"
                        )
                        skipped += 1
                        continue

                    should_send = False
                    title = ""
                    body = ""
                    update_data = {}

                    # =================================================
                    # 1 HOUR REMINDER
                    # =================================================

                    if (
                        diff_minutes <= 60
                        and diff_minutes > 55
                        and not booking.get(
                            "reminder_1hr_sent"
                        )
                    ):
                        should_send = True

                        title = (
                            "Upcoming Service Reminder"
                        )

                        body = (
                            f"Hi {staff_name} 👋\n\n"
                            "Just a reminder that you have "
                            "a service booking in 1 hour ⏰\n\n"
                            "Please get ready and plan your "
                            "travel accordingly.\n\n"
                            "Have a great service session 😊"
                        )

                        update_data = {
                            "reminder_1hr_sent": True,
                        }

                        print(
                            "✅ 1 HOUR REMINDER TRIGGERED"
                        )

                    # =================================================
                    # 30 MIN REMINDER
                    # =================================================

                    if (
                        diff_minutes <= 30
                        and diff_minutes > 25
                        and not booking.get(
                            "reminder_30min_sent"
                        )
                    ):
                        should_send = True

                        title = (
                            "Service Starting Soon"
                        )

                        body = (
                            f"Hi {staff_name} 👋\n\n"
                            "Your service booking will start "
                            "in 30 minutes ⏰\n\n"
                            "Please start your travel and be "
                            "ready for the service.\n\n"
                            "All the best 😊"
                        )

                        update_data = {
                            "reminder_30min_sent": True,
                        }

                        print(
                            "✅ 30 MIN REMINDER TRIGGERED"
                        )

                    if not should_send:
                        continue

                    # =================================================
                    # EXPO PUSH
                    # =================================================

                    print(
                        "📲 Sending reminder to:",
                        assigned_staff_email,
                    )

                    expo_payload = {
                        "to": push_token,
                        "sound": "default",
                        "title": title,
                        "body": body,
                        "priority": "high",
                        "data": {
                            "screen": "new-services",
                            "booking_id": booking.get("id"),
                            "type": "service_reminder",
                        },
                    }

                    expo_response = await client.post(
                        EXPO_PUSH_URL,
                        json=expo_payload,
                    )

                    print(
                        "📩 EXPO STATUS:",
                        expo_response.status_code,
                    )

                    try:
                        expo_data = (
                            expo_response.json()
                        )
                        print(
                            "📩 EXPO RESPONSE:",
                            expo_data,
                        )
                    except Exception:
                        expo_data = None

                    if not expo_response.is_success:
                        print(
                            "❌ Expo push failed:",
                            expo_response.text,
                        )

                        errors += 1
                        continue

                    # =================================================
                    # STORE NOTIFICATION
                    # =================================================

                    notification_data = {
                        "staff_email":
                            assigned_staff_email,

                        "title":
                            title,

                        "body":
                            body,

                        "type":
                            "service_reminder",

                        "is_read":
                            False,

                        "booking_id":
                            booking.get("id"),

                        "customer_name":
                            booking.get("customer_name"),

                        "booking_time":
                            booking.get("booking_time"),

                        "booking_date":
                            booking.get("booking_date"),

                        "services":
                            booking.get("services"),

                        "full_address":
                            booking.get("full_address"),

                        "phone_number":
                            booking.get("phone_number"),
                    }

                    (
                        BookingReminderRepository
                        .create_notification(
                            notification_data
                        )
                    )

                    print(
                        "✅ Notification stored in DB"
                    )

                    # =================================================
                    # UPDATE REMINDER FLAG
                    # =================================================

                    (
                        BookingReminderRepository
                        .update_reminder_flags(
                            booking_id=str(
                                booking.get("id")
                            ),
                            update_data=update_data,
                        )
                    )

                    print(
                        "✅ Reminder flag updated"
                    )

                    sent += 1

                except Exception as error:
                    errors += 1

                    print(
                        "❌ BOOKING ERROR:",
                        str(error),
                    )

        print(
            "🏁 BOOKING REMINDER JOB FINISHED",
            {
                "processed": processed,
                "sent": sent,
                "skipped": skipped,
                "errors": errors,
            },
        )

        return {
            "success": True,
            "processed": processed,
            "sent": sent,
            "skipped": skipped,
            "errors": errors,
        }