"""Tools for the Economic Resilience ADK Agent.

Implements required custom tools:
1. Traversal & cascade exposure query over BigQuery Property Graph.
2. Grant recommendation & impact calculation (turning graph paths into fund allocations).
"""

import os
from typing import Any, Dict, List, Optional
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("PROJECT_ID", ""))
DATASET = os.environ.get("BIGQUERY_DATASET", "a4i_econ")
GRAPH_NAME = f"{DATASET}.LocalEconomy"


def query_cascade_exposure(
    business_id: str,
    max_depth: int = 2,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Queries BigQuery Property Graph using GQL to find downstream cascade exposure.

    Genuine multi-hop graph traversal (:Supplies->{1,max_depth}) from a seed business.

    Args:
        business_id: The unique identifier of the seed business.
        max_depth: Depth of graph traversal (recommended 1 to 2; default is 2).
        project_id: Optional GCP project ID to override environment default.

    Returns:
        A dict containing seed business details, total reachable businesses,
        and downstream exposure paths.
    """
    client = bigquery.Client(project=project_id or PROJECT_ID)
    
    # Genuine GQL graph traversal query over BigQuery Property Graph
    gql_query = f"""
    GRAPH {GRAPH_NAME}
    MATCH p = (seed:Business WHERE seed.business_id = @seed_id)
              -[:Supplies]->{{1,{max_depth}}}(exposed:Business)
    RETURN seed.business_id AS seed_id,
           seed.name AS seed_name,
           seed.naics4 AS seed_industry,
           exposed.business_id AS exposed_id,
           exposed.name AS exposed_name,
           exposed.naics4 AS exposed_industry,
           TO_JSON(p) AS path_json
    LIMIT 100
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("seed_id", "STRING", business_id)
        ]
    )

    try:
        query_job = client.query(gql_query, job_config=job_config)
        results = [dict(row) for row in query_job.result()]
        
        exposed_ids = {r["exposed_id"] for r in results}
        seed_name = results[0]["seed_name"] if results else "Unknown"

        return {
            "seed_id": business_id,
            "seed_name": seed_name,
            "max_depth": max_depth,
            "exposed_business_count": len(exposed_ids),
            "records": results,
            "status": "success",
        }
    except Exception as e:
        return {
            "seed_id": business_id,
            "error": str(e),
            "status": "failed",
            "hint": "Check that BigQuery reservation with Enterprise edition exists and graph is built.",
        }


def evaluate_grant_recommendation(
    seed_business_id: str,
    exposed_count: int,
    total_fund_budget: float = 50000.0,
    requested_amount: float = 10000.0,
    is_critical_hub: bool = False,
) -> Dict[str, Any]:
    """Custom logic turning graph cascade exposure paths into a reasoned funding recommendation.

    A graph makes consequence visible; this tool performs the decision weighting:
    - Balances hub exposure vs fragile downstream dependency.
    - Decides grant sizing relative to protected downstream businesses and available budget.

    Args:
        seed_business_id: The identifier of the applicant business.
        exposed_count: Number of unique businesses exposed in cascade traversal.
        total_fund_budget: Total micro-grant fund budget available (default $50,000).
        requested_amount: Amount requested by applicant (default $10,000).
        is_critical_hub: Whether the business is an extreme hub (> 25 connections).

    Returns:
        Structured grant recommendation with recommended amount, priority tier, and rationale.
    """
    if exposed_count == 0:
        recommended_amount = 0.0
        priority = "LOW"
        rationale = "Zero downstream businesses identified in supply chain cascade."
    elif is_critical_hub or exposed_count > 25:
        # Avoid automatically funding giant hubs which are typically already well-capitalized
        recommended_amount = min(requested_amount, 7500.0)
        priority = "MEDIUM"
        rationale = (
            f"High connectivity ({exposed_count} downstream), but caution against hub bias: "
            "verify whether alternative suppliers exist before full capital commitment."
        )
    elif 5 <= exposed_count <= 25:
        # Sweet spot for community resilience: high multiplier, non-obvious cascade
        recommended_amount = min(requested_amount, total_fund_budget * 0.25)
        priority = "HIGH"
        rationale = (
            f"Optimal resilience target: protects {exposed_count} downstream businesses "
            "in the sweet spot (5-25) where closure triggers a severe, localized cascade."
        )
    else:
        # 1 to 4 downstream businesses
        recommended_amount = min(requested_amount, 5000.0)
        priority = "MODERATE"
        rationale = f"Moderate local cascade protecting {exposed_count} businesses."

    return {
        "business_id": seed_business_id,
        "priority": priority,
        "recommended_amount": recommended_amount,
        "max_fund_budget": total_fund_budget,
        "downstream_protected_count": exposed_count,
        "rationale": rationale,
    }
