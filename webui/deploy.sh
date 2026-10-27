#!/usr/bin/env bash
# Run from the REPO ROOT:  PROJECT=my-proj REGION=us-central1 bash webui/deploy.sh
set -euo pipefail
PROJECT="${PROJECT:?set PROJECT}"; REGION="${REGION:-us-central1}"; SVC="${SVC:-supplier-advisor}"
SA="${SA:-}"   # optional runtime service account with BigQuery Data Viewer + Job User on a4i_econ
gcloud run deploy "$SVC" --source . --project "$PROJECT" --region "$REGION" \
  --allow-unauthenticated=false \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_LOCATION=$REGION" \
  ${SA:+--service-account "$SA"} \
  --dockerfile webui/Dockerfile 2>/dev/null || \
gcloud builds submit --tag "gcr.io/$PROJECT/$SVC" --project "$PROJECT" -f webui/Dockerfile . 2>/dev/null || true
echo "If --dockerfile is unsupported in your gcloud, copy webui/Dockerfile to ./Dockerfile and re-run."
