"""Scripted DEMO agent for trying the web UI without BigQuery or Gemini.

It replays a fixed tool sequence with MOCK data shaped like the real tools in agent/tools.py.
All names and numbers are invented. Never use it for real recommendations.
"""
import json
from typing import Any, Dict, Optional

from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types


def discover_priority_candidates(min_exposed: int = 5, max_exposed: int = 25, industry_prefix: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
    """MOCK: candidates in the exposure band."""
    c = [
        {"business_id": "M-101", "business_name": "Example Flour Works", "industry": "3118", "exposed_2hop": 14, "is_sole_source_in_corridor": True, "corridor_peers_in_naics": 1, "caveat": "Generator artifact: sole registrant in corridor NAICS; buyers could source externally"},
        {"business_id": "M-102", "business_name": "Example Cold Brew Co", "industry": "3121", "exposed_2hop": 9, "is_sole_source_in_corridor": False, "corridor_peers_in_naics": 4, "caveat": "Competitive local industry cluster"},
        {"business_id": "M-103", "business_name": "Example Candle Studio", "industry": "3399", "exposed_2hop": 6, "is_sole_source_in_corridor": False, "corridor_peers_in_naics": 3, "caveat": "Competitive local industry cluster"},
    ]
    return {"candidate_count": len(c), "candidates": c, "sweet_spot_band": f"{min_exposed}-{max_exposed}", "status": "success"}


def query_cascade_exposure(business_id: str, max_depth: int = 2) -> Dict[str, Any]:
    """MOCK: cascade for one seed."""
    def node(i, name):
        return {"kind": "node", "identifier": i, "labels": ["Business"], "properties": {"business_id": i, "name": name}}
    def edge(a, b, w):
        return {"kind": "edge", "labels": ["Supplies"], "properties": {"intensity": w}, "source_node_identifier": a, "destination_node_identifier": b}
    paths = [
        json.dumps([node("M-101", "Example Flour Works"), edge("M-101", "M-201", .34), node("M-201", "Example Cafe One"), edge("M-201", "M-301", .2), node("M-301", "Example Event Hall")]),
        json.dumps([node("M-101", "Example Flour Works"), edge("M-101", "M-202", .28), node("M-202", "Example Deli"), edge("M-202", "M-302", .15), node("M-302", "Example Lunch Counter")]),
    ]
    return {
        "seed_id": business_id, "seed_name": "Example Flour Works", "seed_naics4": "3118", "max_depth": max_depth,
        "total_downstream_exposed_count": 5, "direct_customers_count": 3, "indirect_customers_count": 2,
        "cascade_multiplier_score": 4.3,
        "direct_customers": [
            {"buyer_id": "M-201", "buyer_name": "Example Cafe One", "buyer_industry": "7225", "seed_intensity": .34, "metres": 120, "total_input_intensity": .62, "supplier_count": 3, "customer_reliance_share": .55},
            {"buyer_id": "M-202", "buyer_name": "Example Deli", "buyer_industry": "7225", "seed_intensity": .28, "metres": 210, "total_input_intensity": .75, "supplier_count": 4, "customer_reliance_share": .37},
            {"buyer_id": "M-203", "buyer_name": "Example Caterer", "buyer_industry": "7223", "seed_intensity": .41, "metres": 340, "total_input_intensity": .6, "supplier_count": 2, "customer_reliance_share": .68},
        ],
        "upstream_suppliers_count": 1, "upstream_suppliers": [{"supplier_id": "M-401", "supplier_name": "Example Grain Mill", "supplier_industry": "3112"}],
        "upstream_single_point_of_failure": True, "sample_paths": paths, "status": "success",
    }


def validate_sba_ground_truth(business_id: str, business_naics4: Optional[str] = None) -> Dict[str, Any]:
    """MOCK: SBA validation."""
    return {"business_id": business_id, "corridor_coverage_percentage": "1.3% (3 of 231 businesses matched)", "direct_loan_match": False, "direct_charged_off": False, "direct_records": [],
            "benchmark_level_used": "CA_NAICS2_ROLLUP_31", "benchmark_sample_size": 412, "benchmark_seasoned_charge_off_rate": 0.042,
            "methodology_disclosures": ["CIRCULARITY GUARD: Validator is context only, never a grant sizing input.", "SELECTION BIAS: SBA borrowers are credit applicants; this is an SBA Industry Credit Benchmark, not total failure rate."], "status": "success"}


def evaluate_grant_recommendation(seed_business_id: str, total_downstream_exposed_count: int, direct_customers_count: int = 0, cascade_multiplier_score: float = 0.0, upstream_suppliers_count: int = 0) -> Dict[str, Any]:
    """MOCK: sizing."""
    return {"business_id": seed_business_id, "priority": "HIGH", "recommended_amount": 12500.0, "cascade_multiplier_score": cascade_multiplier_score, "is_hub_penalized": False, "is_sole_source_artifact": True,
            "rationale": "Prime resilience target: protects 5 downstream venues (3 direct buyers). CAUTION: applicant has single upstream supplier. (Note: sole registrant in corridor NAICS - reach is upper bound).", "status": "success"}


def allocate_portfolio_grants(candidates: list, total_fund_budget: float = 50000.0) -> Dict[str, Any]:
    """MOCK: portfolio."""
    return {"total_budget": total_fund_budget, "total_allocated": 21500.0, "unallocated_reserve": 28500.0, "funded_count": 2, "runner_up_count": 1,
            "funded_portfolio": [{"business_id": "M-101", "business_name": "Example Flour Works", "recommended_amount": 12500.0, "allocated_amount": 12500.0, "cascade_multiplier_score": 4.3, "status": "FUNDED"},
                                 {"business_id": "M-102", "business_name": "Example Cold Brew Co", "recommended_amount": 9000.0, "allocated_amount": 9000.0, "cascade_multiplier_score": 3.1, "status": "FUNDED"}],
            "runner_ups": [{"business_id": "M-103", "business_name": "Example Candle Studio", "cascade_multiplier_score": 1.2, "status": "RUNNER_UP", "reason": "Trailing multiplier score."}], "status": "success"}


def audit_corridor_equity_and_portfolio_bias(funded_business_ids: list) -> Dict[str, Any]:
    """MOCK: equity audit."""
    return {"portfolio_size": 2, "funded_avg_tract_poverty": 0.248, "corridor_avg_poverty": 0.216, "equity_status": "EQUITABLE: Portfolio prioritizes higher-than-average poverty tracts.",
            "industry_breakdown": {"funded_producers": 2, "funded_food_service": 0, "corridor_total_producers": 31, "corridor_total_food_service": 96}, "transit_reliance_no_vehicle_pct": 0.41, "status": "success"}


_MEMO = """### Micro-Grant Triage Memo (DEMO, MOCK DATA)
**Business**: Example Flour Works (ID: M-101, NAICS 3118)

#### 1. Network cascade and protection value
- 3 direct customers, 2 indirect; cascade score 4.3 (intensity-weighted)
- Single upstream supplier: **yes** (Example Grain Mill)

#### 2. Hub and generator-artifact check
- Sole registrant in its industry: reach is an **upper bound**.

#### 3. SBA validation (context only)
- No direct loan record. Benchmark: CA NAICS2 rollup, n=412, 4.2%. Not used to size the grant.

#### 4. Recommendation
- **Fund $12,500**, priority HIGH. Runner-up: Example Candle Studio.

#### 5. Honest disclosure
- Supply links are **modeled** from industry averages, not observed contracts.
- Cash reserves, inventory and off-corridor suppliers are unobserved.
"""

_SCRIPT = [
    ("discover_priority_candidates", {"min_exposed": 5, "max_exposed": 25, "industry_prefix": "31"}),
    ("query_cascade_exposure", {"business_id": "M-101", "max_depth": 2}),
    ("validate_sba_ground_truth", {"business_id": "M-101", "business_naics4": "3118"}),
    ("evaluate_grant_recommendation", {"seed_business_id": "M-101", "total_downstream_exposed_count": 5, "direct_customers_count": 3, "cascade_multiplier_score": 4.3, "upstream_suppliers_count": 1}),
    ("allocate_portfolio_grants", {"candidates": [{"business_id": "M-101"}, {"business_id": "M-102"}, {"business_id": "M-103"}], "total_fund_budget": 50000.0}),
    ("audit_corridor_equity_and_portfolio_bias", {"funded_business_ids": ["M-101", "M-102"]}),
]


class ScriptedLlm(BaseLlm):
    model: str = "scripted-demo"

    async def generate_content_async(self, llm_request, stream=False):
        done = sum(1 for c in llm_request.contents for p in (c.parts or []) if p.function_response)
        if done < len(_SCRIPT):
            name, args = _SCRIPT[done]
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name=name, args=args))]))
        else:
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=_MEMO)]))


root_agent = Agent(
    name="demo_agent",
    model=ScriptedLlm(),
    description="Scripted demo of the resilience agent tool flow (MOCK data).",
    instruction="Demo only.",
    tools=[discover_priority_candidates, query_cascade_exposure, validate_sba_ground_truth, evaluate_grant_recommendation, allocate_portfolio_grants, audit_corridor_equity_and_portfolio_bias],
)
