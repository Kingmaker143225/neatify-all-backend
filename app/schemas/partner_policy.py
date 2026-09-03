from pydantic import BaseModel


class PolicyResponse(BaseModel):
    user_policies: str | None = None
    terms_and_conditions: str | None = None


class AcceptPolicyResponse(BaseModel):
    success: bool


class PolicyStatusResponse(BaseModel):
    terms_accepted: bool
    privacy_policy_accepted: bool