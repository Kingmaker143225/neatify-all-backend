from fastapi import APIRouter

from app.services.booking_reminder_service import (
    BookingReminderService,
)


router = APIRouter()


@router.post("/booking-reminders/run")
async def run_booking_reminders():

    return await (
        BookingReminderService
        .process_reminders()
    )