from app.config import settings
from supabase import Client, create_client

supabase: Client = create_client(settings.supabase_url, settings.supabase_key)


async def insert_lead(data: dict) -> bool:
    try:
        supabase.table("leads").insert(data).execute()
        return True
    except Exception:
        return False
