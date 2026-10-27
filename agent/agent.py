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

from .tools import (
    evaluate_grant_recommendation,
    query_cascade_exposure,
    read_dataset_table,
    write_grant_decision,
)

# MCP Toolbox server URL if configured (e.g., Cloud Run or local container)
MCP_TOOLBOX_URL = os.environ.get("MCP_TOOLBOX_URL")

tools = [
    query_cascade_exposure,
    evaluate_grant_recommendation,
    read_dataset_table,
    write_grant_decision,
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
for small businesses in San Francisco's **Central Market corridor**, specifically focusing on the **micro-producer track**
(artisanal food/beverage makers, bakeries, light craft manufacturing [NAICS 31-33], commercial kitchens, and local suppliers).

Your mission:
Decide micro-grant allocations not merely based on direct individual distress, but on **cascade protection**
across Central Market's local production and supply web. Micro-producers act as critical anchor suppliers
for cafes, restaurants, and neighborhood storefronts.

Guiding Principles:
1. **"A graph makes consequence visible; it does not make the decision."**
2. **Anchor Multiplier vs. Hub Bias**:
   - Giant generic hubs (>25 downstream connections, e.g. ubiquitous broadline vendors) are robust and easily substitutable.
   - Genuine micro-producers with 5–25 downstream connections represent high-leverage resilience targets: their closure removes specialized local inputs that ripple through multiple downstream neighborhood venues.
3. **Data Integrity & Modeling Reality**:
   - `businesses` and SBA `borrowed_from` records (including charge-offs/failures) are 100% ground-truth.
   - `supplies` edges are modeled from BEA industry input-output rates bounded by walkable corridor distance (<=1200m). Explicitly state confidence and assumptions in your evaluation memo.
4. **Execution Workflow**:
   - Use `query_cascade_exposure` (or MCP tools) to traverse the BigQuery Property Graph (`a4i_econ.LocalEconomy`) at 1-2 hops.
   - Use `evaluate_grant_recommendation` to size grants relative to downstream businesses protected.
   - Generate an audit-ready, structured grant memo covering:
     * Business & Micro-Producer Profile (Sector, NAICS, Corridor location)
     * Downstream Exposure Cascade (Reachable businesses, critical dependencies)
     * Resilience Grant Recommendation ($ amount, priority tier, decision rationale)
     * Model Assumptions, Caveats & Equity/Tract Context
   - Record formal decisions using `write_grant_decision` when approved.
""",

# root_agent is the required ADK entry point
root_agent = Agent(
    name="resilience_grant_agent",
    model=os.environ.get("ADK_MODEL", "gemini-2.5-flash"),
    description="Agent for evaluating small business micro-grants via BigQuery property graph cascade analysis.",
    instruction=AGENT_INSTRUCTION,
    tools=tools,
)
