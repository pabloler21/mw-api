import httpx

from app.config import settings


async def send_lead_notification(lead_data: dict) -> bool:
    """Send lead notification email via Resend."""
    if not settings.resend_api_key:
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.resend_api_key}"},
            json={
                "from": "leads@mwgloballink.com",
                "to": ["info@mwgloballink.com"],
                "subject": f"New lead: {lead_data.get('empresa', 'Unknown')}",
                "text": str(lead_data),
            },
        )
        return response.status_code == 200
