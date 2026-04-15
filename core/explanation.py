from __future__ import annotations

from api.models import DecisionResult, RiskResult
from api.schemas import PredictionRequest


def generate_explanation(
    request: PredictionRequest,
    risk: RiskResult,
    decision: DecisionResult,
) -> str:
    factors = ", ".join(risk.top_factors[:5])

    if risk.risk_level == "high":
        return (
            f"Risk is elevated due to {factors}. "
            f"The estimated confidence is {risk.confidence:.2f}, so the system recommends: "
            f"{decision.recommendation}. "
            "Clinician review is advised to support safe decision-making."
        )

    if risk.risk_level == "medium":
        return (
            f"Risk is moderate based on {factors}. "
            f"The estimated confidence is {risk.confidence:.2f}. "
            f"The recommended next step is: {decision.recommendation}."
        )

    return (
        f"Current risk appears lower, based mainly on {factors}. "
        f"The estimated confidence is {risk.confidence:.2f}. "
        f"The recommended approach is: {decision.recommendation}."
    )