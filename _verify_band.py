"""Verify Band provider integration across all workflow tiers."""
import httpx
import json

BASE = "http://localhost:8001"

print("=" * 60)
print("BAND PROVIDER INTEGRATION VERIFICATION")
print("=" * 60)

# 1. Band status
print("\n--- BAND STATUS ---")
r = httpx.get(f"{BASE}/band/status", timeout=10)
status = r.json()
print(json.dumps(status, indent=2))

# 2. Workflows
for tier in ["low", "medium", "high"]:
    body = {
        "identity": {
            "agent_id": f"band_verify_{tier}",
            "owner": "verifier",
            "model": "gpt-4o",
            "purpose": f"Band integration verify - {tier}",
        },
        "tier": tier,
    }
    print(f"\n--- {tier.upper()} TIER WORKFLOW ---")
    try:
        resp = httpx.post(f"{BASE}/workflow", json=body, timeout=60)
        data = resp.json()
        wf_status = data.get("status", "unknown")
        wf_error = data.get("error")
        metrics = data.get("execution_metrics", [])
        providers = {m["agent_name"]: m["provider"] for m in metrics}

        print(f"  Status:  {wf_status}")
        print(f"  Error:   {wf_error}")
        print(f"  Agents executed: {len(metrics)}")
        for agent, prov in providers.items():
            tag = " <-- Band target" if agent in ("ComplianceAgent", "RiskAgent", "AuditAgent") else ""
            print(f"    {agent}: provider={prov}{tag}")
    except Exception as e:
        print(f"  FAILED: {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
