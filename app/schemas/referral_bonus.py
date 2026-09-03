from pydantic import BaseModel


class ReferralBonusRequest(BaseModel):
    referrer_phone: str
    referrer_name: str
    referred_friend_name: str
    bonus_amount: str