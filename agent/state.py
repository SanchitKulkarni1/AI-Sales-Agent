from typing import TypedDict

class LeadState(TypedDict):
    lead_id: int
    raw_data: dict

    rule_score: float
    ml_score: float
    final_score: float
    tier: str

    context: list
    explanation: str
