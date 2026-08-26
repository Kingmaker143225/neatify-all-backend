from pydantic import BaseModel


class ReferralRewardRequest(BaseModel):
    staff_name: str
    referred_person_name: str
    amount: str
    phone: str