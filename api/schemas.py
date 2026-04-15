from typing import List, Optional

from pydantic import BaseModel, Field


class PatientPreferences(BaseModel):
    avoid_hospital: bool = Field(default=False, description="Whether the patient prefers to avoid hospital escalation where possible")
    cost_sensitive: bool = Field(default=False, description="Whether the patient is cost sensitive")
    prefers_remote: bool = Field(default=True, description="Whether the patient prefers remote-first care when clinically appropriate")


class PredictionRequest(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    age: int = Field(..., ge=0, le=120)
    heart_rate: float = Field(..., ge=20, le=250)
    hrv: float = Field(..., ge=0, le=300, description="Heart rate variability")
    sleep_hours: float = Field(..., ge=0, le=24)
    steps: int = Field(..., ge=0)
    spo2: float = Field(..., ge=50, le=100)
    symptoms: str = Field(..., min_length=1)
    medical_history: List[str] = Field(default_factory=list)
    patient_preferences: PatientPreferences = Field(default_factory=PatientPreferences)
    clinician_override_requested: bool = Field(default=False)


class PredictionResponse(BaseModel):
    patient_id: str
    risk_score: float
    confidence: float
    risk_level: str
    recommendation: str
    recommended_action: str
    explanation: str
    top_factors: List[str]
    clinician_review_required: bool


class HealthResponse(BaseModel):
    status: str
    service: str