from agent.graph import graph
from db.session import SessionLocal
from db.models import Lead, LeadScore, LeadExplanation
from pprint import pprint

sample_lead = {
    "TotalVisits": 8,
    "Total Time Spent on Website": 250,
    "Page Views Per Visit": 4,
    "Last Activity": "Email Opened",
    "Last Notable Activity": "Email Opened",
    "What is your current occupation": "Working Professional",
    "Specialization": "IT",
    "Do Not Call": "No",
    "Do Not Email": "No"
}

db = SessionLocal()

# 1. Store raw lead
lead = Lead(raw_data=sample_lead)
db.add(lead)
db.commit()
db.refresh(lead)

# 2. Run agent
result = graph.invoke({
    "lead_id": lead.id,
    "raw_data": lead.raw_data
})

# 3. Store scores
score = LeadScore(
    lead_id=lead.id,
    rule_score=result["rule_score"],
    ml_score=result["ml_score"],
    final_score=result["final_score"],
    tier=result["tier"]
)

# 4. Store explanation
explanation = LeadExplanation(
    lead_id=lead.id,
    context=result["context"],
    explanation=result["explanation"]
)

db.add_all([score, explanation])
db.commit()

pprint(result)
