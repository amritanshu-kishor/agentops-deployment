"""Full backend verification for governance endpoint, workflows, and endpoints."""
import httpx
import json
import os

BASE = "http://localhost:8001"

print("=" * 60)
print("GOVERNANCE BACKEND VALIDATION")
print("=" * 60)

# Task 6: Verify endpoints
print("\n--- TASK 6: ENDPOINT VERIFICATION ---")
endpoints = [
    ("/health", "Health"),
    ("/integration/status", "Integration Status"),
    ("/agents", "Runtime Agents"),
    ("/agents/governance", "Governance Agents"),
    ("/band/status", "Band Status"),
]

results = {}
for path, label in endpoints:
    try:
        r = httpx.get(f"{BASE}{path}", timeout=10)
        results[path] = r.json()
        print(f"  {label:25s} -> {r.status_code} OK")
    except Exception as e:
        results[path] = None
        print(f"  {label:25s} -> FAILED: {e}")

# Print governance agents
print("\n--- GOVERNANCE AGENTS RESPONSE ---")
gov = results.get("/agents/governance", [])
for a in gov:
    print(f"  {a['agent_id']:20s} provider={a['provider']:8s} type={a['type']:6s} tier={a['tier']}")

# Print band status
print("\n--- BAND STATUS ---")
print(json.dumps(results.get("/band/status", {}), indent=2))

# Task 7: Workflow verification
print("\n--- TASK 7: WORKFLOW VERIFICATION ---")
for tier in ["low", "medium", "high"]:
    body = {
        "identity": {
            "agent_id": f"gov_test_{tier}",
            "owner": "governance_validator",
            "model": "gpt-4o",
            "purpose": f"Governance validation - {tier}",
        },
        "tier": tier,
    }
    try:
        resp = httpx.post(f"{BASE}/workflow", json=body, timeout=60)
        data = resp.json()
        metrics = data.get("execution_metrics", [])
        agents_run = [m["agent_name"] for m in metrics]
        providers = {m["agent_name"]: m["provider"] for m in metrics}

        print(f"\n  {tier.upper()} TIER:")
        print(f"    Status: {data.get('status')}")
        print(f"    Error:  {data.get('error')}")
        print(f"    Agents: {agents_run}")
        for agent, prov in providers.items():
            tag = ""
            if agent in ("ComplianceAgent", "RiskAgent", "AuditAgent"):
                tag = " [Band target]"
            print(f"      {agent}: {prov}{tag}")
    except Exception as e:
        print(f"\n  {tier.upper()} TIER: FAILED - {e}")

# Save governance JSON for screenshot evidence
os.makedirs("reports/screenshots", exist_ok=True)
with open("reports/governance_response.json", "w") as f:
    json.dump(gov, f, indent=2)
with open("reports/band_status.json", "w") as f:
    json.dump(results.get("/band/status", {}), f, indent=2)

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)
