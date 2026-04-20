# MW Global Link — Backend

FastAPI backend for MW Global Link. MVP handles lead form submissions (email via Resend + Supabase storage). Designed to grow into an AI orchestration layer (chatbot, prospection agents, RAG).

## Stack

- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Validation:** Pydantic v2 + pydantic-settings
- **Email:** Resend
- **Database:** Supabase (PostgreSQL)
- **Linting:** Ruff
- **Tests:** pytest + pytest-asyncio
- **Deployment:** Render

## Dev Commands

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies (including dev extras)
pip install -e ".[dev]"

# Run dev server (port 8000, auto-reload)
uvicorn app.main:app --reload

# Run tests
pytest

# Lint
ruff check .
ruff format .
```

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app, CORS, router registration
│   ├── config.py         # Settings via pydantic-settings (.env)
│   ├── api/
│   │   ├── leads.py      # POST /api/leads — MVP form submission
│   │   ├── chat.py       # Post-MVP: AI chatbot
│   │   └── bunker.py     # Future: private dashboard API
│   ├── agents/           # Post-MVP: LangChain agents
│   ├── services/
│   │   ├── email.py      # Resend integration
│   │   └── calendar.py   # Calendly webhook handler (Post-MVP)
│   └── models/
│       └── lead.py       # Pydantic schema for lead
├── tests/
│   └── test_leads.py
├── pyproject.toml
├── Dockerfile
├── render.yaml
└── .env.example
```

## Environment Variables

Copy `.env.example` → `.env`:

```
DEBUG=false
RESEND_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

## Key Conventions

- All settings loaded via `app/config.py` (`pydantic-settings`). Never hardcode secrets.
- Routers registered in `app/main.py` with `/api` prefix.
- Pydantic models in `app/models/`. One file per domain entity.
- Services in `app/services/`. Each service is a plain module with async functions.
- `asyncio_mode = "auto"` — all tests can be `async def`.
- Ruff line length: 88. Import order enforced (`I` rule).

## API Endpoints

| Method | Path         | Description              |
|--------|--------------|--------------------------|
| GET    | /health      | Health check             |
| POST   | /api/leads   | Submit contact/lead form |

## Deployment

Deployed on **Render** (see `render.yaml`). The `backend/` directory is the root for the Render service.

## Jira

- **URL:** https://lernerpb.atlassian.net
- **Proyecto:** MGL (mw global link, ID: 10033)
- **Email:** lerner.pb@gmail.com
- **Credenciales guardadas en:** `C:\Users\pablo\.claude\projects\C--Users-pablo-Desktop-bot-curriculum\memory\reference_jira.md`

Para consultar issues desde PowerShell:

```powershell
$token = '<API_TOKEN>'
$email = 'lerner.pb@gmail.com'
$pair = $email + ':' + $token
$creds = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$headers = @{Authorization='Basic ' + $creds; Accept='application/json'; 'Content-Type'='application/json'}
$body = @{jql='project = MGL AND status = "In Progress"'; fields=@('summary','status','assignee')} | ConvertTo-Json
$r = Invoke-RestMethod -Uri 'https://lernerpb.atlassian.net/rest/api/3/search/jql' -Method POST -Headers $headers -Body $body
$r.issues | ForEach-Object { "$($_.key) - $($_.fields.summary)" }
```
