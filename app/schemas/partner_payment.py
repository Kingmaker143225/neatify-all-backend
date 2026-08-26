from pydantic import BaseModel


class PartnerPaymentRequest(BaseModel):
    staff_name: str
    amount: float
    phone: str
    date: str