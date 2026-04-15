from fastapi import FastAPI

from api.schemas import HealthResponse, PredictionRequest, PredictionResponse
from core.decision_engine import generate_decision
from core.explanation import generate_explanation
from core.risk_model import compute_risk

app = FastAPI(
    title="HCAI-Triage API",
    version="0.1.0",
    description="A human-centred AI triage prototype for remote primary care and early warning.",
)


@app.get("/", response_model=HealthResponse)
def root() -> HealthResponse:
    return HealthResponse(status="ok", service="HCAI-Triage API")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="HCAI-Triage API")


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    risk = compute_risk(request)
    decision = generate_decision(request, risk)
    explanation = generate_explanation(request, risk, decision)

    return PredictionResponse(
        patient_id=request.patient_id,
        risk_score=risk.risk_score,
        confidence=risk.confidence,
        risk_level=risk.risk_level,
        recommendation=decision.recommendation,
        recommended_action=decision.recommended_action,
        explanation=explanation,
        top_factors=risk.top_factors,
        clinician_review_required=decision.clinician_review_required,
    )