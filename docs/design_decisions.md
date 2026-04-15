# Design Decisions

## Purpose
This project is a production-oriented prototype of a human-centred AI triage system for remote primary care and early warning.

It is designed to demonstrate:
- modular AI system design
- safe recommendation logic
- explainability
- clinician oversight
- deployment-oriented backend engineering

## Why a rule-based starter prototype?
The original coursework concept includes:
- multimodal data fusion
- Bayesian reasoning
- sequential decision-making
- preference-sensitive recommendations
- explainability
- clinician-in-the-loop oversight

For an initial engineering prototype, this repository uses:
- structured clinical signals
- interpretable scoring logic
- confidence estimation
- recommendation rules
- modular architecture

This keeps the system:
- easy to understand
- easy to test
- easy to extend
- suitable for portfolio demonstration

## Current Modules
### 1. Risk Model
The risk model combines:
- physiological signals
- symptom keywords
- medical history

This simulates an interpretable prediction layer.

### 2. Decision Engine
The decision engine translates risk levels into actionable recommendations such as:
- monitor
- GP review
- urgent assessment

### 3. Explainability Layer
The explanation layer turns structured outputs into readable reasoning for patients or clinicians.

### 4. Clinician Review Logic
The system supports clinician review escalation and override requests.

## Future Engineering Extensions
- replace rules with a trained model
- add SHAP-based feature importance
- support structured longitudinal patient state
- introduce probabilistic calibration
- add audit logging
- integrate EHR/FHIR workflows
- deploy with CI/CD and observability

## Human-Centred AI Principles
This prototype is guided by:
- safety
- transparency
- interpretability
- human oversight
- patient-centred support