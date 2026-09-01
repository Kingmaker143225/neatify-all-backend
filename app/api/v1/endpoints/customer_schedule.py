# app/api/v1/endpoints/customer_schedule.py

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

# ✅ Import Supabase client
from app.supabase.client import supabase

# ✅ Create router
router = APIRouter()


# =========================================================
# SCHEMAS
# =========================================================

class ScheduleConfigResponse(BaseModel):
    config_key: str
    config_value: any


class BookingsDateResponse(BaseModel):
    bookings: list


class HubResolveRequest(BaseModel):
    pincode: str
    address: Optional[str] = ""


class HubResolveResponse(BaseModel):
    hub_name: Optional[str] = None
    is_active: bool = True


class StaffCountResponse(BaseModel):
    count: int = 0


# =========================================================
# SCHEDULE CONFIG
# =========================================================

@router.get("/schedule-config")
async def get_schedule_config():
    """
    Get schedule configuration (time slots, years, etc.)
    """
    try:
        response = supabase.table("schedule_config").select("*").execute()
        
        if response.data:
            # Convert to a more usable format
            config_dict = {}
            for item in response.data:
                config_dict[item.get("config_key")] = item.get("config_value")
            return config_dict
        
        # Return defaults if no config found
        return {
            "time_slots": [
                "9:00 am", "9:30 am", "10:00 am", "10:30 am",
                "11:00 am", "11:30 am", "12:00 pm",
                "1:00 pm", "1:30 pm", "2:00 pm", "2:30 pm",
                "3:00 pm", "3:30 pm", "4:00 pm", "4:30 pm"
            ],
            "years": [2026, 2027, 2028],
            "date_time_slots": {},
            "service_time_rules": []
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch schedule config: {str(e)}"
        )


# =========================================================
# BOOKINGS BY DATE
# =========================================================

@router.get("/bookings/date", response_model=BookingsDateResponse)
async def get_bookings_by_date(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
):
    """
    Get active bookings for a specific date.
    Excludes cancelled and failed payment bookings.
    """
    try:
        # Get bookings for the date
        response = supabase.table("bookings") \
            .select("*") \
            .eq("booking_date", date) \
            .execute()
        
        # Filter active bookings
        active_bookings = []
        for booking in response.data or []:
            work_status = str(booking.get("work_status") or "").upper()
            payment_status = str(booking.get("payment_status") or "").upper()
            
            # Skip cancelled or failed payment bookings
            if work_status == "CANCELLED" or payment_status == "FAILED":
                continue
            
            active_bookings.append(booking)
        
        return BookingsDateResponse(bookings=active_bookings)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch bookings: {str(e)}"
        )


# =========================================================
# RESOLVE HUB FROM LOCATION
# =========================================================

@router.post("/hubs/resolve", response_model=HubResolveResponse)
async def resolve_hub(
    request: HubResolveRequest,
):
    """
    Resolve hub from pincode and/or address.
    """
    try:
        clean_pin = "".join(filter(str.isdigit, request.pincode))[:6]
        address_upper = request.address.upper() if request.address else ""
        
        hub_name = None
        is_active = True
        
        # 1. Match by pincode in hub_locations table
        if len(clean_pin) == 6:
            response = supabase.table("hub_locations") \
                .select("hub_name, location_name, is_active") \
                .eq("pincode", clean_pin) \
                .execute()
            
            if response.data and len(response.data) > 0:
                # Try to find specific location match
                if address_upper:
                    for loc in response.data:
                        loc_name = (loc.get("location_name") or "").upper().strip()
                        if loc_name and loc_name in address_upper:
                            return HubResolveResponse(
                                hub_name=loc.get("hub_name"),
                                is_active=loc.get("is_active") != False
                            )
                
                # Return first active match
                active_match = next(
                    (loc for loc in response.data if loc.get("is_active") != False),
                    response.data[0]
                )
                return HubResolveResponse(
                    hub_name=active_match.get("hub_name"),
                    is_active=active_match.get("is_active") != False
                )
        
        # 2. Fallback: Match by location_name in address
        if address_upper:
            response = supabase.table("hub_locations") \
                .select("hub_name, location_name, is_active") \
                .execute()
            
            if response.data:
                for loc in response.data:
                    loc_name = (loc.get("location_name") or "").upper().strip()
                    if loc_name and loc_name in address_upper:
                        return HubResolveResponse(
                            hub_name=loc.get("hub_name"),
                            is_active=loc.get("is_active") != False
                        )
        
        # No hub found
        return HubResolveResponse(hub_name=None, is_active=False)
        
    except Exception as e:
        print(f"❌ Error resolving hub: {str(e)}")
        return HubResolveResponse(hub_name=None, is_active=False)


# =========================================================
# GET HUB STAFF COUNT
# =========================================================

@router.get("/hubs/{hub_name}/staff-count", response_model=StaffCountResponse)
async def get_hub_staff_count(
    hub_name: str,
    category: str = Query(..., description="Service category"),
):
    """
    Get staff count for a specific hub and category.
    """
    try:
        response = supabase.table("hub_category_counts") \
            .select("count, category, hub") \
            .eq("hub", hub_name) \
            .ilike("category", f"%{category}%") \
            .execute()
        
        if response.data and len(response.data) > 0:
            # Find the best match
            category_upper = category.upper().strip()
            
            for item in response.data:
                cat = (item.get("category") or "").upper().strip()
                # Check if category matches exactly or is contained
                if cat == category_upper or category_upper in cat or cat in category_upper:
                    try:
                        count = int(item.get("count") or 0)
                        return StaffCountResponse(count=count)
                    except (ValueError, TypeError):
                        pass
            
            # Return first match
            try:
                count = int(response.data[0].get("count") or 0)
                return StaffCountResponse(count=count)
            except (ValueError, TypeError):
                pass
        
        return StaffCountResponse(count=0)
        
    except Exception as e:
        print(f"❌ Error fetching staff count: {str(e)}")
        return StaffCountResponse(count=0)