from __future__ import annotations

from typing import List, Tuple

from api.models import RiskResult
from api.schemas import PredictionRequest


SYMPTOM_WEIGHTS = {
    "shortness of breath": 0.22,
    "chest pain": 0.30,
    "fatigue": 0.08,
    "dizziness": 0.12,
    "fever": 0.10,
    "confusion": 0.20,
    "palpitations": 0.16,
    "fainting": 0.25,
    "cough": 0.06,
}


HISTORY_WEIGHTS = {
    "hypertension": 0.07,
    "diabetes": 0.08,
    "copd": 0.12,
    "asthma": 0.08,
    "heart disease": 0.15,
    "chronic kidney disease": 0.12,
    "obesity": 0.06,
}


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _contains_symptom(symptoms_text: str, symptom_key: str) -> bool:
    return symptom_key.lower() in symptoms_text.lower()


def _risk_level_from_score(score: float) -> str:
    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def _calculate_base_signal_risk(request: PredictionRequest) -> Tuple[float, List[str]]:
    score = 0.0
    factors: List[str] = []

    if request.heart_rate >= 110:
        score += 0.20
        factors.append("very high heart rate")
    elif request.heart_rate >= 100:
        score += 0.14
        factors.append("high heart rate")
    elif request.heart_rate <= 50:
        score += 0.14
        factors.append("abnormally low heart rate")

    if request.hrv < 20:
        score += 0.16
        factors.append("very low HRV")
    elif request.hrv < 30:
        score += 0.10
        factors.append("low HRV")

    if request.sleep_hours < 4:
        score += 0.12
        factors.append("very low sleep")
    elif request.sleep_hours < 6:
        score += 0.08
        factors.append("low sleep")

    if request.steps < 2000:
        score += 0.10
        factors.append("low activity")
    elif request.steps < 4000:
        score += 0.05
        factors.append("reduced activity")

    if request.spo2 < 92:
        score += 0.28
        factors.append("low oxygen saturation")
    elif request.spo2 < 95:
        score += 0.14
        factors.append("borderline oxygen saturation")

    if request.age >= 75:
        score += 0.12
        factors.append("older age")
    elif request.age >= 60:
        score += 0.07
        factors.append("elevated age-related risk")

    return score, factors


def _calculate_symptom_risk(symptoms_text: str) -> Tuple[float, List[str]]:
    score = 0.0
    factors: List[str] = []

    for symptom, weight in SYMPTOM_WEIGHTS.items():
        if _contains_symptom(symptoms_text, symptom):
            score += weight
            factors.append(symptom)

    return score, factors


def _calculate_history_risk(history: List[str]) -> Tuple[float, List[str]]:
    score = 0.0
    factors: List[str] = []

    history_normalised = [item.strip().lower() for item in history]

    for condition, weight in HISTORY_WEIGHTS.items():
        if condition in history_normalised:
            score += weight
            factors.append(condition)

    return score, factors


def _bayesian_style_confidence_adjustment(base_score: float, factor_count: int) -> float:
    """
    Simplified confidence adjustment inspired by uncertainty-aware reasoning.
    More supporting factors slightly increase confidence, but confidence stays bounded.
    """
    confidence = 0.55 + (0.05 * min(factor_count, 5)) + (0.15 * base_score)
    return _clamp(round(confidence, 2), 0.50, 0.95)


def compute_risk(request: PredictionRequest) -> RiskResult:
    base_score, signal_factors = _calculate_base_signal_risk(request)
    symptom_score, symptom_factors = _calculate_symptom_risk(request.symptoms)
    history_score, history_factors = _calculate_history_risk(request.medical_history)

    raw_score = base_score + symptom_score + history_score
    risk_score = _clamp(round(raw_score, 2))
    top_factors = signal_factors + symptom_factors + history_factors

    if not top_factors:
        top_factors = ["limited clinical risk signals identified"]

    confidence = _bayesian_style_confidence_adjustment(risk_score, len(top_factors))
    risk_level = _risk_level_from_score(risk_score)

    return RiskResult(
        risk_score=risk_score,
        confidence=confidence,
        risk_level=risk_level,
        top_factors=top_factors[:5],
    )