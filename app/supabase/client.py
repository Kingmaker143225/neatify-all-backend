from supabase import create_client, Client

from app.config.settings import settings


supabase: Client = create_client(
    supabase_url=settings.supabase_url,
    supabase_key=settings.supabase_service_role_key,
)