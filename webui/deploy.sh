#!/usr/bin/env bash
# Run from the REPO ROOT:  PROJECT=my-proj REGION=us-central1 bash webui/deploy.sh
set -euo pipefail
PROJECT="${PROJECT:-qwiklabs-gcp-03-14e29f4c8c1f}"; REGION="${REGION:-us-central1}"; SVC="${SVC:-supplier-advisor}"
SA="${SA:-supplier-advisor-sa@qwiklabs-gcp-03-14e29f4c8c1f.iam.gserviceaccount.com}"

gcloud run deploy "$SVC" \
  --source . \
  --project "$PROJECT" \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300 \
  --service-account "$SA" \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_LOCATION=$REGION,BIGQUERY_DATASET=a4i_econ"
