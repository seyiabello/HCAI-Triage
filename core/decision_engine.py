from __future__ import annotations

from api.models import DecisionResult, RiskResult
from api.schemas import PredictionRequest


def generate_decision(request: PredictionRequest, risk: RiskResult) -> DecisionResult:
    prefers_remote = request.patient_preferences.prefers_remote
    avoid_hospital = request.patient_preferences.avoid_hospital

    if request.clinician_override_requested:
        return DecisionResult(
            recommendation="Clinician review requested",
            recommended_action="Hold automated recommendation pending clinician assessment",
            clinician_review_required=True,
        )

    if risk.risk_score >= 0.85:
        return DecisionResult(
            recommendation="Urgent GP review within 24 hours",
            recommended_action="Escalate for clinician assessment",
            clinician_review_required=True,
        )

    if risk.risk_score >= 0.65:
        if prefers_remote and not avoid_hospital:
            return DecisionResult(
                recommendation="Same-day remote or in-person GP assessment",
                recommended_action="Arrange urgent clinician follow-up",
                clinician_review_required=True,
            )
        return DecisionResult(
            recommendation="Urgent GP review",
            recommended_action="Escalate for clinician assessment",
            clinician_review_required=True,
        )

    if risk.risk_score >= 0.45:
        if prefers_remote:
            return DecisionResult(
                recommendation="Remote GP review within 48 hours",
                recommended_action="Schedule clinician follow-up and continue monitoring",
                clinician_review_required=True,
            )
        return DecisionResult(
            recommendation="GP review within 48 hours",
            recommended_action="Schedule follow-up and continue monitoring",
            clinician_review_required=True,
        )

    return DecisionResult(
        recommendation="Continue monitoring with self-management guidance",
        recommended_action="Provide monitoring advice and safety-net instructions",
        clinician_review_required=False,
    )