# Advisor web UI (same-service)

One FastAPI process serves the UI at `/ui/` and the ADK API (`/list-apps`, `/apps/.../sessions`, `/run_sse`). No CORS, one Cloud Run service.

## Place in the repo
Copy this `webui/` folder to the repo root, next to `agent/`:
```
repo/
  agent/        (ADK package: agent.py with root_agent)
  webui/        (this folder)
```

## Run locally against the REAL agent
```
pip install -r webui/requirements.txt
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT=<project>  GOOGLE_GENAI_USE_VERTEXAI=TRUE  GOOGLE_CLOUD_LOCATION=us-central1
# optional: export MCP_TOOLBOX_URL=http://localhost:5000
uvicorn webui.server:app --port 8080
```
Open http://localhost:8080/ . The UI auto-selects app `agent`; use `?app=<name>` to pick another.

## Run with no BigQuery/Gemini (demo agent, MOCK data)
```
AGENTS_DIR=webui/dev_agents uvicorn webui.server:app --port 8080
```

## Deploy to Cloud Run
From repo root: `PROJECT=<id> bash webui/deploy.sh` (or `gcloud run deploy --source .` after copying webui/Dockerfile to ./Dockerfile). Runtime service account needs BigQuery Job User and Data Viewer on `a4i_econ`. Keep `--allow-unauthenticated=false` for a hackathon demo unless judges need a public link.

## Env vars
`AGENTS_DIR` (default repo root), `ALLOW_ORIGINS`, `SESSION_DB_URI` (default in-memory; sessions are lost on restart), `GOOGLE_CLOUD_PROJECT`, `MCP_TOOLBOX_URL`.

## What the UI reads from tool results
Evidence panel keys off tool names and return shapes in `agent/tools.py`: `query_cascade_exposure`, `validate_sba_ground_truth`, `evaluate_grant_recommendation`, `audit_corridor_equity_and_portfolio_bias`, `assess_footfall_commuter_exposure`, `discover_priority_candidates`, `allocate_portfolio_grants`. If you rename a tool or field, update `ingest()` / `renderEvidence()` in `static/index.html`. Hop-2 nodes come from `sample_paths` (TO_JSON path); confirm the real shape once against BigQuery.

## Caveats
Cannot test the real agent from here (needs your BigQuery and Gemini). The UI is verified against ADK 2.13 event shapes with the scripted demo agent. The model decides which tools to call, so panels fill only for tools it actually uses.
