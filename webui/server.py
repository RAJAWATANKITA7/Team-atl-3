"""Single-service host: ADK API + the custom web UI.

Run locally from the repo root:
    pip install -r webui/requirements.txt
    uvicorn webui.server:app --port 8080
then open http://localhost:8080/

AGENTS_DIR must be the folder that CONTAINS the agent package (the repo root, which holds `agent/`).
Set AGENTS_DIR=webui/dev_agents to try the UI with a scripted demo agent (no BigQuery or Gemini needed).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from google.adk.cli.fast_api import get_fast_api_app

HERE = Path(__file__).resolve().parent
# Load .env from repo root if it exists
load_dotenv(HERE.parent / ".env")

AGENTS_DIR = os.environ.get("AGENTS_DIR", str(HERE.parent))
# Same-origin by default (UI and API share one URL), so no CORS is needed.
# Set ALLOW_ORIGINS="https://a.example,https://b.example" only if the UI is hosted elsewhere.
ALLOW_ORIGINS = [o for o in os.environ.get("ALLOW_ORIGINS", "").split(",") if o] or None
# Optional persistent sessions, e.g. sqlite+aiosqlite:///./sessions.db (default: in memory).
SESSION_DB_URI = os.environ.get("SESSION_DB_URI") or None

app = get_fast_api_app(
    agents_dir=AGENTS_DIR,
    web=False,                      # we ship our own UI; the ADK developer UI stays off
    allow_origins=ALLOW_ORIGINS,
    session_service_uri=SESSION_DB_URI,
)


@app.get("/", include_in_schema=False)
def _root() -> RedirectResponse:
    return RedirectResponse("/ui/")


@app.get("/healthz", include_in_schema=False)
def _health() -> dict:
    return {"status": "ok"}


app.mount("/ui", StaticFiles(directory=HERE / "static", html=True), name="ui")
