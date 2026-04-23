import logging
from datetime import datetime, timezone

import resend

from app.config import settings
from app.models.lead import LeadCreate

logger = logging.getLogger(__name__)


def _build_subject(lead: LeadCreate) -> str:
    return f"Nuevo Lead MW Global Link: {lead.product} — {lead.company}"


def _build_text(lead: LeadCreate, timestamp: str) -> str:
    lines = [
        "Nuevo lead recibido en MW Global Link",
        "",
        f"Nombre:            {lead.name}",
        f"Empresa:           {lead.company}",
        f"Email:             {lead.email}",
        f"Puerto de destino: {lead.destination_port or '—'}",
        f"Producto:          {lead.product}",
        f"Mensaje:           {lead.message or '—'}",
        f"Timestamp:         {timestamp}",
        "",
        "Ver leads en Supabase:",
        f"{settings.supabase_url}/project/default/editor",
    ]
    return "\n".join(lines)


def _row(label: str, value: str) -> str:
    return (
        f"<tr><td style='padding:8px 12px 8px 0;color:#888'>{label}</td>"
        f"<td style='padding:8px 0'><strong>{value}</strong></td></tr>"
    )


def _build_html(lead: LeadCreate, timestamp: str) -> str:
    supabase_url = settings.supabase_url
    btn = "background:#0070f3;color:#fff;padding:10px 20px"
    btn += ";border-radius:6px;text-decoration:none"
    return f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto">
      <h2 style="color:#0070f3;margin-bottom:4px">Nuevo Lead — MW Global Link</h2>
      <p style="color:#666;margin-top:0">{timestamp}</p>
      <table style="border-collapse:collapse;width:100%;margin-top:16px">
        {_row("Nombre", lead.name)}
        {_row("Empresa", lead.company)}
        {_row("Email", str(lead.email))}
        {_row("Puerto de destino", lead.destination_port or "—")}
        {_row("Producto", lead.product)}
        {_row("Mensaje", lead.message or "—")}
      </table>
      <p style="margin-top:24px">
        <a href="{supabase_url}/project/default/editor" style="{btn}">
          Ver en Supabase
        </a>
      </p>
    </div>
    """


async def send_lead_notification(lead: LeadCreate) -> bool:
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not set — skipping email notification")
        return False

    if not settings.ceo_email:
        logger.warning("CEO_EMAIL not set — skipping email notification")
        return False

    resend.api_key = settings.resend_api_key
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [settings.ceo_email],
            "subject": _build_subject(lead),
            "text": _build_text(lead, timestamp),
            "html": _build_html(lead, timestamp),
        })
        return True
    except Exception as e:
        logger.error("Failed to send lead notification email: %s", e)
        return False
