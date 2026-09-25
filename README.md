# 🧠 AI Sales Agent: Explainable Lead Qualification

Sales teams waste time on leads that were never going to convert. This agent scores every lead with a **hybrid engine (ML + business rules + LLM)**, sorts it into **HOT / WARM / COLD**, and writes a **grounded explanation** of each decision, so reps know *why* a lead is a priority and not just that it is.

## How it works

The pipeline is a LangGraph state machine:

```
rule ──▶ ml ──▶ final ──▶ context ──▶ explain
```

| Node | What it does |
|---|---|
| `rule` | Deterministic score from engagement (visits, time on site, pages per visit), intent (last activity), authority (occupation) and penalties (Do-Not-Call / Do-Not-Email). |
| `ml` | Conversion probability from a scikit-learn Logistic Regression pipeline trained on historical lead data. ID and leakage columns are dropped before training. |
| `final` | Blended score `0.6 × ML + 0.4 × rules`. Tiers: **HOT ≥ 0.75**, **WARM ≥ 0.45**, otherwise **COLD**. |
| `context` | Retrieves the relevant sales playbook rules from a ChromaDB vector store. |
| `explain` | Gemini writes a 3-part rationale: *why this tier*, *risks / caveats*, *recommended next action*. It is grounded in the scores and the retrieved playbook. |

Leads, scores and explanations are persisted with SQLAlchemy (SQLite by default; you can swap it for Postgres).

## Features

- **Single-lead scoring:** fill in a form and get the tier, all three scores and the explanation instantly.
- **Batch CSV scoring:** upload a CSV of leads and score them all asynchronously.
- **Explainable by design:** every tier comes with its reasoning, risks and next step.

## Tech stack

Python · LangGraph · scikit-learn · ChromaDB · Google Gemini (`google-genai`) · SQLAlchemy · Streamlit · pandas

## Project structure

```
agent/          LangGraph state, nodes and graph
llm/            Gemini client and prompt templates
vectorstore/    ChromaDB ingestion + retriever
db/             SQLAlchemy models and session
rule_scoring.py Business-rule scoring
data_train.py   Model training script
batch_score.py  CLI batch scoring
app.py          Streamlit UI
```

## Run locally

```bash
pip install streamlit pandas scikit-learn joblib langgraph chromadb google-genai sqlalchemy python-dotenv
echo "GOOGLE_API_KEY=your_key" > .env

python data_train.py        # (optional) retrain lead_conversion_model.pkl
python vectorstore/ingest.py # (optional) rebuild the playbook vector store
python db/init_db.py        # create tables
streamlit run app.py
```

A sample input file is provided at `data/sample_testing.csv`.
