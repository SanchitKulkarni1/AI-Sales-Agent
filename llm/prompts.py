def build_explanation_prompt(state):
    return f"""
You are a sales operations analyst.

Your job is to explain WHY a lead was classified the way it was.
Do NOT change the decision.
Do NOT invent new facts.

Lead Tier: {state['tier']}
Final Score: {state['final_score']}
ML Score (conversion likelihood): {state['ml_score']}
Rule Score (business urgency): {state['rule_score']}

Business Context:
{chr(10).join(state['context'])}

Lead Signals:
- Last Activity: {state['raw_data'].get('Last Activity')}
- Total Visits: {state['raw_data'].get('TotalVisits')}
- Time Spent on Website: {state['raw_data'].get('Total Time Spent on Website')}
- Occupation: {state['raw_data'].get('What is your current occupation')}

Explain in:
1. Why this tier was assigned
2. Any risks or caveats
3. Recommended next action

Keep it concise and factual.
"""
