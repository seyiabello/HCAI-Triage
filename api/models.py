from dataclasses import dataclass
from typing import List


@dataclass
class RiskResult:
    risk_score: float
    confidence: float
    risk_level: str
    top_factors: List[str]


@dataclass
class DecisionResult:
    recommendation: str
    recommended_action: str
    clinician_review_required: bool