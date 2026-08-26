from fastapi import APIRouter, HTTPException

from app.services.system_service import SystemService

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Neatify Backend"
    }


@router.get("/supabase-test")
async def supabase_test():
    try:
        data = SystemService.test_connection()

        return {
            "success": True,
            "message": "Supabase Connected Successfully",
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )