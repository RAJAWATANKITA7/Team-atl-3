# Build from the REPO ROOT so both agent/ and webui/ are in the image:
#   docker build -f webui/Dockerfile -t advisor .
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PORT=8080
COPY webui/requirements.txt /tmp/req.txt
RUN pip install --no-cache-dir -r /tmp/req.txt \
 && ( [ -f /app/agent/requirements.txt ] || true )
COPY agent /app/agent
COPY webui /app/webui
# agents_dir = /app (contains the agent/ package ADK will discover as app "agent")
ENV AGENTS_DIR=/app
EXPOSE 8080
CMD ["sh","-c","uvicorn webui.server:app --host 0.0.0.0 --port ${PORT}"]
