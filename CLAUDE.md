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
- **Deployment:** Render (Python runtime, no Docker)

## Branching Strategy

```
feature/xxx → development → master
```

- **Feature branches** van SIEMPRE a `development`, NUNCA a `master`.
- `master` solo recibe merges desde `development`.
- Cada push a `development` o `master` dispara el CI/CD completo.

## Environments

| Entorno | Rama | Render Service | Supabase |
|---|---|---|---|
| Development | `development` | `mw-global-link-api-dev` | proyecto dev |
| Production | `master` | `mw-global-link-api` | proyecto prod |

La variable `APP_ENV` controla qué archivo `.env` carga `config.py` localmente:
- `APP_ENV=development` → `.env.development`
- `APP_ENV=production` → `.env.production`
- No definida → `.env`

En Render, las variables de entorno se inyectan directamente (sin archivo).

## CI/CD — GitHub Actions (`backend.yml`)

Flujo por push a cualquier rama protegida:

1. **Lint & Test** — siempre corre, usa secrets `DEV_*`
2. **Push Migrations** — solo en push (no PRs), usa secrets del entorno correspondiente
3. **Deploy** — solo en push, después de migrations, trigger via deploy hook de Render

Auto-deploy está **deshabilitado** en ambos servicios de Render — el CI controla cuándo se deploya.

### GitHub Secrets requeridos

| Secret | Uso |
|---|---|
| `DEV_SUPABASE_URL` | Tests |
| `DEV_SUPABASE_KEY` | Tests |
| `DEV_RESEND_API_KEY` | Tests |
| `DEV_CEO_EMAIL` | Tests |
| `DEV_SUPABASE_PROJECT_REF` | Migrations dev |
| `DEV_SUPABASE_ACCESS_TOKEN` | Migrations dev |
| `DEV_SUPABASE_DB_PASSWORD` | Migrations dev |
| `SUPABASE_PROJECT_REF` | Migrations prod |
| `SUPABASE_ACCESS_TOKEN` | Migrations prod |
| `SUPABASE_DB_PASSWORD` | Migrations prod |
| `RENDER_DEPLOY_HOOK_DEV` | Deploy dev |
| `RENDER_DEPLOY_HOOK_PROD` | Deploy prod |

## Dev Commands

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Instalar dependencias (incluyendo dev extras)
pip install -e ".[dev]"

# Correr servidor dev (puerto 8000, auto-reload)
APP_ENV=development uvicorn app.main:app --reload

# Correr tests
pytest

# Lint
ruff check .
ruff format .
```

## Project Structure

```
app/
├── main.py           # FastAPI app, CORS, router registration
├── config.py         # Settings via pydantic-settings (env_file dinámico por APP_ENV)
├── api/
│   ├── leads.py      # POST /api/leads — MVP form submission
│   ├── chat.py       # Post-MVP: AI chatbot
│   └── bunker.py     # Future: private dashboard API
├── agents/           # Post-MVP: LangChain agents
├── services/
│   ├── email.py      # Resend integration
│   └── calendar.py   # Calendly webhook handler (Post-MVP)
└── models/
    └── lead.py       # Pydantic schema for lead
tests/
pyproject.toml
render.yaml           # Define ambos servicios (prod + dev), autoDeploy: false
```

## Environment Variables

Usar `.env.development` para desarrollo local y `.env.production` para producción.
Ambos archivos están en `.gitignore` — nunca se commitean.

Variables requeridas:

```
APP_ENV=           # development | production
DEBUG=
RESEND_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
ALLOWED_ORIGINS=   # JSON array o comma-separated: ["url1","url2"] o url1,url2
CEO_EMAIL=
```

## Key Conventions

- Todos los settings se cargan via `app/config.py` (`pydantic-settings`). Nunca hardcodear secrets.
- Routers registrados en `app/main.py` con prefijo `/api`.
- Modelos Pydantic en `app/models/`. Un archivo por entidad de dominio.
- Servicios en `app/services/`. Cada servicio es un módulo con funciones async.
- `asyncio_mode = "auto"` — todos los tests pueden ser `async def`.
- Ruff line length: 88. Import order enforced (regla `I`).

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check (incluye APP_ENV) |
| POST | /api/leads | Submit contact/lead form |

## Jira

- **URL:** https://lernerpb.atlassian.net
- **Proyecto:** MGL (ID: 10033)
- **Credenciales:** `C:\Users\pablo\.claude\projects\C--Users-pablo-Desktop-mw-global-link\memory\reference_jira.md`
