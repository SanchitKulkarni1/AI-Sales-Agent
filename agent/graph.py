from langgraph.graph import StateGraph
from agent.state import LeadState
from agent.nodes import (
    rule_scoring_node,
    ml_scoring_node,
    final_scoring_node,
    retrieve_context_node,
    explanation_node
)

builder = StateGraph(LeadState)

builder.add_node("rule", rule_scoring_node)
builder.add_node("ml", ml_scoring_node)
builder.add_node("final", final_scoring_node)
builder.add_node("context", retrieve_context_node)
builder.add_node("explain", explanation_node)

builder.set_entry_point("rule")
builder.add_edge("rule", "ml")
builder.add_edge("ml", "final")
builder.add_edge("final", "context")
builder.add_edge("context", "explain")

graph = builder.compile()
