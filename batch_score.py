import pandas as pd
import asyncio

from agent.graph import graph
from db.session import SessionLocal
from db.models import Lead, LeadScore, LeadExplanation
from llm.gemini_client import generate_explanation
from llm.prompts import build_explanation_prompt

db = SessionLocal()

async def process_row(row):
    raw_data = row.to_dict()

    # 1. Store lead
    lead = Lead(raw_data=raw_data)
    db.add(lead)
    db.commit()
    db.refresh(lead)

    # 2. Run deterministic pipeline (SYNC)
    state = graph.invoke({
        "lead_id": lead.id,
        "raw_data": raw_data
    })

    # 3. Gemini explanation (ASYNC)
    prompt = build_explanation_prompt(state)
    explanation = await generate_explanation(prompt)

    # 4. Persist results
    db.add(LeadScore(
        lead_id=lead.id,
        rule_score=state["rule_score"],
        ml_score=state["ml_score"],
        final_score=state["final_score"],
        tier=state["tier"]
    ))

    db.add(LeadExplanation(
        lead_id=lead.id,
        context=state["context"],
        explanation=explanation
    ))

    db.commit()

async def main():
    df = pd.read_csv("Lead Scoring.csv")

    tasks = [process_row(row) for _, row in df.iterrows()]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
