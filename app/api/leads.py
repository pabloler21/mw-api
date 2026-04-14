from fastapi import APIRouter

from app.models.lead import LeadCreate, LeadResponse

router = APIRouter()


@router.post("/leads", response_model=LeadResponse)
async def submit_lead(lead: LeadCreate) -> LeadResponse:
    # TODO: save to Supabase and send email via Resend
    return LeadResponse(success=True, message="Lead received successfully")
