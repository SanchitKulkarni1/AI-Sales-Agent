from rule_scoring import compute_rule_score
from vectorstore.retriever import retrieve_context
from agent.state import LeadState
from llm.gemini_client import generate_explanation
from llm.prompts import build_explanation_prompt
import pandas as pd
import joblib
import pandas as pd

def rule_scoring_node(state: LeadState):
    score = compute_rule_score(state["raw_data"])
    state["rule_score"] = score
    return state


model = joblib.load("lead_conversion_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

def ml_scoring_node(state):
    # Create DataFrame with ALL required columns
    df = pd.DataFrame(columns=feature_columns)

    # Insert current lead values
    df.loc[0] = {col: state["raw_data"].get(col, None) for col in feature_columns}

    ml_score = model.predict_proba(df)[0][1]
    state["ml_score"] = round(float(ml_score), 3)

    return state

def final_scoring_node(state: LeadState):
    final = 0.6 * state["ml_score"] + 0.4 * state["rule_score"]
    state["final_score"] = round(final, 3)

    if final >= 0.75:
        state["tier"] = "HOT"
    elif final >= 0.45:
        state["tier"] = "WARM"
    else:
        state["tier"] = "COLD"

    return state

def retrieve_context_node(state):
    query = f"Why is a lead classified as {state['tier']}?"
    context = retrieve_context(query)

    state["context"] = context
    return state

async def explanation_node(state: LeadState):
    prompt = build_explanation_prompt(state)
    explanation = await generate_explanation(prompt) 

    state["explanation"] = explanation
    return state
    return state
