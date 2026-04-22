from supabase import create_client, Client

from app.config import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_key)


async def insert_lead(data: dict) -> bool:
    try:
        supabase.table("leads").insert(data).execute()
        return True
    except Exception:
        return False
