import httpx

from fastapi import HTTPException

from app.supabase.admin_client import supabase_admin


EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


class NotificationService:

    @staticmethod
    async def send_to_token(
        token: str,
        title: str | None = None,
        body: str | None = None,
        data: dict | None = None,
    ):
        if not token:
            raise HTTPException(
                status_code=400,
                detail="Push token is required.",
            )

        message = {
            "to": token,
            "sound": "default",
            "title": title or "Neatify Staff",
            "body": body or "You have a new update.",
            "data": data or {},
        }

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(
                    EXPO_PUSH_URL,
                    json=message,
                    headers={
                        "Content-Type": "application/json",
                    },
                )

            if response.status_code >= 400:
                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": "Expo push notification failed.",
                        "expo_response": response.text,
                    },
                )

            try:
                result = response.json()
            except Exception:
                result = {
                    "raw_response": response.text
                }

            return {
                "success": True,
                "data": result,
            }

        except httpx.RequestError as error:
            raise HTTPException(
                status_code=502,
                detail=f"Unable to connect to Expo Push API: {str(error)}",
            )

    @staticmethod
    async def send_to_staff_email(
        email: str,
        title: str | None = None,
        body: str | None = None,
        data: dict | None = None,
    ):
        if not email:
            raise HTTPException(
                status_code=400,
                detail="Staff email is required.",
            )

        # =========================================================
        # FIND STAFF PUSH TOKEN
        # =========================================================

        response = (
            supabase_admin
            .table("staff_profile")
            .select("push_token,email,name")
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        staff = response.data

        if not staff:
            raise HTTPException(
                status_code=404,
                detail="Staff profile not found.",
            )

        push_token = staff.get("push_token")

        if not push_token:
            raise HTTPException(
                status_code=400,
                detail="No push token found for this staff member.",
            )

        # =========================================================
        # SEND PUSH
        # =========================================================

        result = await NotificationService.send_to_token(
            token=push_token,
            title=title,
            body=body,
            data=data,
        )

        return {
            "success": True,
            "email": email,
            "staff_name": staff.get("name"),
            "push_token_found": True,
            "notification": result,
        }