from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.supabase.client import supabase


router = APIRouter()


@router.get("/referral/validate")
async def validate_referral_code(
    code: str,
    current_customer=Depends(get_current_customer),
):
    clean_code = code.strip().upper()

    if not clean_code:
        return {
            "valid": False,
            "referrer_id": None,
        }

    response = (
        supabase
        .table("profile")
        .select("id")
        .eq("referral_code", clean_code)
        .maybe_single()
        .execute()
    )

    if not response.data:
        return {
            "valid": False,
            "referrer_id": None,
        }

    return {
        "valid": True,
        "referrer_id": response.data["id"],
    }