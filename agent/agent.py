"""ADK Agent Definition for Economic Resilience & Micro-Grants.

Complies with challenge requirements:
- Built with Google ADK in Python.
- Exposes `root_agent` entrypoint.
- Uses Gemini 2.5 Flash / Gemini model for reasoning & memo generation.
- Integrates custom Python tools (cascade exposure query & grant impact weighting).
- Supports MCP Toolbox integration for managed database tools.
"""

from __future__ import annotations

import os
from google.adk.agents import Agent

from .tools import query_cascade_exposure, evaluate_grant_recommendation

# MCP Toolbox server URL if configured (e.g., Cloud Run or local container)
MCP_TOOLBOX_URL = os.environ.get("MCP_TOOLBOX_URL")

tools = [
    query_cascade_exposure,
    evaluate_grant_recommendation,
]

# If an MCP Toolbox is running, connect ToolboxToolset
if MCP_TOOLBOX_URL:
    try:
        from google.adk.tools.toolbox_toolset import ToolboxToolset

        toolbox = ToolboxToolset(server_url=MCP_TOOLBOX_URL)
        tools.append(toolbox)
    except Exception as e:
        print(f"Warning: Could not connect to MCP Toolbox at {MCP_TOOLBOX_URL}: {e}")

AGENT_INSTRUCTION = """\
You are an expert Economic Development & Resilience Grant Officer evaluating micro-grant applications
for businesses in a San Francisco commercial corridor (e.g. Central Market).

Your goal:
Decide micro-grant allocations not merely based on direct need, but on **cascade protection**
across the corridor's supply network.

Guiding Principles:
1. "A graph makes a consequence visible; it does not make the decision."
2. Hubs (central nodes with >25 connections) are not automatically the best investment—they are often robust.
   The highest leverage grants typically sit in the 5–25 downstream exposed band.
3. Two of the edge types are modeled based on BEA industry coefficients, so acknowledge the degree of confidence
   and what assumptions you are making.
4. When queried about a business:
   - Call `query_cascade_exposure` with depth 1 or 2 to trace real multi-hop reachability via BigQuery Property Graph.
   - Call `evaluate_grant_recommendation` to convert the cascade metrics into an actionable grant amount and priority tier.
   - Formulate a clear, audit-ready grant memo detailing:
     * Applicant Profile & Corridor context
     * Downstream exposure & critical dependencies
     * Grant recommendation amount & justification
     * Model assumptions and caveats
"""

# root_agent is the required ADK entry point
root_agent = Agent(
    name="resilience_grant_agent",
    model=os.environ.get("ADK_MODEL", "gemini-2.5-flash"),
    description="Agent for evaluating small business micro-grants via BigQuery property graph cascade analysis.",
    instruction=AGENT_INSTRUCTION,
    tools=tools,
)
