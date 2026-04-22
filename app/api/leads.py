from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request

from app.models.lead import LeadCreate, LeadResponse
from app.services.email import send_lead_notification
from app.services.supabase import insert_lead

router = APIRouter()

_rate_limit: dict[str, list[datetime]] = {}


@router.post("/leads", response_model=LeadResponse)
async def submit_lead(lead: LeadCreate, request: Request) -> LeadResponse:
    ip = request.client.host
    now = datetime.now(timezone.utc)

    timestamps = [t for t in _rate_limit.get(ip, []) if (now - t).seconds < 3600]
    if len(timestamps) >= 5:
        raise HTTPException(
            status_code=429, detail="Too many requests. Try again later."
        )
    _rate_limit[ip] = timestamps + [now]

    data = lead.model_dump()

    saved = await insert_lead(data)
    if not saved:
        raise HTTPException(status_code=500, detail="Failed to save lead.")

    await send_lead_notification(data)

    return LeadResponse(success=True, message="Thanks! We'll be in touch soon.")
