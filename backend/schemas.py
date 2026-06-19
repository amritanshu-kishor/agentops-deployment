from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class HealthResponse(BaseModel):
    status: str
    config_loaded: bool
    database: str
    redis: str


class IntegrationStatusResponse(BaseModel):
    supabase: str
    redis: str
    tables_created: bool
    seed_data: bool
    workflows: Dict[str, int]
    total_workflows: int
    audit_logs: int
    cost_records: int
    cost_tracking: bool
    audit_logs_working: bool
    integration_complete: bool


class TestAIRequest(BaseModel):
    prompt: str


class TestAIResponse(BaseModel):
    status: str
    provider: str
    response: str
    error: Optional[str] = None


class TestBandRequest(BaseModel):
    action: str  # create_room, send_message, get_messages, close_room
    room_name: Optional[str] = None
    room_id: Optional[str] = None
    message: Optional[str] = None


class TestBandResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    error: Optional[str] = None


# ── Workflow response schemas ──────────────────────────────────────────────────

class WorkflowResponse(BaseModel):
    id: str
    agent_id: str
    owner: str
    model: str
    purpose: str
    status: str
    tier: str
    band_room_id: Optional[str] = None
    band_execution_id: Optional[str] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    final_decision: Optional[str] = None

    model_config = {"from_attributes": True}


class WorkflowDetailResponse(WorkflowResponse):
    transient_state: Optional[Dict[str, Any]] = None


class AuditLogResponse(BaseModel):
    id: str
    workflow_id: str
    event_type: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

    model_config = {"from_attributes": True}


class RiskLogResponse(BaseModel):
    id: str
    workflow_id: str
    risk_score: int
    severity: str
    findings: Optional[List[Any]] = None
    recommendation: str
    rationale: str
    score_breakdown: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PerformanceLogResponse(BaseModel):
    id: str
    workflow_id: str
    agent_name: str
    provider: str
    latency_ms: float
    success: bool
    error_message: Optional[str] = None
    timestamp: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CostLogResponse(BaseModel):
    id: str
    workflow_id: str
    agent_name: str
    provider: str
    model: str
    estimated_tokens: int
    estimated_cost_usd: float
    timestamp: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AgentSummaryResponse(BaseModel):
    agent_id: str
    owner: str
    model: str
    purpose: str
    tier: str

    model_config = {"from_attributes": True}
