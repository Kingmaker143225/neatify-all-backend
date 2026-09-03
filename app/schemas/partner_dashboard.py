from pydantic import BaseModel


class BookingStats(BaseModel):
    new: int
    assigned: int
    completed: int
    cancelled: int


class DutyStats(BaseModel):
    is_available: bool
    today_minutes: int
    weekly_minutes: int
    monthly_minutes: int


class EarningsStats(BaseModel):
    total: float
    weekly: float
    monthly: float


class PartnerDashboardResponse(BaseModel):
    success: bool
    bookings: BookingStats
    duty: DutyStats
    earnings: EarningsStats