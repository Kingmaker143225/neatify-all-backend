# app/api/v1/endpoints/customer_offers.py

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.supabase.client import supabase

router = APIRouter()

class ActiveOfferResponse(BaseModel):
    offer_percentage: Optional[int] = None
    title: Optional[str] = None

@router.get("/offers/active")
async def get_active_offer(
    service_title: str = Query(..., description="Title of the service to check for offers"),
):
    """
    Get active offer percentage for a specific service by title.
    """
    try:
        response = supabase.table("offers") \
            .select("offer_percentage, title") \
            .eq("title", service_title) \
            .eq("is_offer_enabled", True) \
            .maybe_single() \
            .execute()
        
        if response.data:
            return ActiveOfferResponse(
                offer_percentage=response.data.get("offer_percentage"),
                title=response.data.get("title")
            )
        
        return ActiveOfferResponse(offer_percentage=None, title=None)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch active offer: {str(e)}"
        )