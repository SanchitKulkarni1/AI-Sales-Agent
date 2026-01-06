import streamlit as st
import pandas as pd
import time
import asyncio

from agent.graph import graph

# =========================================================
# Helpers
# =========================================================
def parse_explanation_sections(explanation: str):
    sections = {"why": "", "risks": "", "action": ""}
    current = None

    for line in explanation.splitlines():
        line = line.strip()

        if line.startswith("### 1"):
            current = "why"
            continue
        elif line.startswith("### 2"):
            current = "risks"
            continue
        elif line.startswith("### 3"):
            current = "action"
            continue

        if current and line:
            sections[current] += line + "\n"

    return sections


def tier_badge(tier: str):
    if tier == "HOT":
        return "🔥 **HOT**"
    elif tier == "WARM":
        return "🟡 **WARM**"
    return "❄️ **COLD**"


def render_lead_card(title, result):
    sections = parse_explanation_sections(result["explanation"])

    with st.container():
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        col1.subheader(title)
        col2.markdown(tier_badge(result["tier"]))

        m1, m2, m3 = st.columns(3)
        m1.metric("Final Score", result["final_score"])
        m2.metric("ML Score", result["ml_score"])
        m3.metric("Rule Score", result["rule_score"])

        st.markdown("#### Why this tier was assigned")
        st.markdown(sections["why"] or "_No explanation provided._")

        st.markdown("#### Risks / Caveats")
        st.markdown(sections["risks"] or "_No risks identified._")

        st.markdown("#### Recommended Next Action")
        st.markdown(sections["action"] or "_No recommendation provided._")

        with st.expander("📌 Business Context Used"):
            for ctx in result["context"]:
                st.markdown(f"- {ctx}")


# =========================================================
# Streamlit Config
# =========================================================
st.set_page_config(
    page_title="Sales Lead Qualification Agent",
    layout="centered"
)

st.title("🧠 Sales Lead Qualification Agent")
st.caption("Hybrid ML + Rules + VectorDB + Gemini 2.0 Flash")

tab1, tab2 = st.tabs(["🔹 Single Lead Scoring", "📁 Batch CSV Scoring"])

# =========================================================
# TAB 1 — SINGLE LEAD SCORING
# =========================================================
with tab1:
    st.subheader("Single Lead Input")

    with st.form("single_lead_form"):
        col1, col2 = st.columns(2)

        with col1:
            total_visits = st.number_input("Total Website Visits", min_value=0, value=5)
            time_spent = st.number_input("Total Time (seconds)", min_value=0, value=200)
            pages_per_visit = st.number_input("Page Views Per Visit", min_value=0.0, value=3.0)
            specialization = st.text_input("Specialization / Domain", "IT")

        with col2:
            last_activity = st.selectbox(
                "Last Activity",
                ["Email Opened", "SMS Sent", "Olark Chat Conversation", "Email Clicked", "Other"]
            )
            occupation = st.selectbox(
                "Occupation",
                ["Working Professional", "Business Owner", "Student", "Unemployed"]
            )
            do_not_call = st.selectbox("Do Not Call", ["No", "Yes"])
            do_not_email = st.selectbox("Do Not Email", ["No", "Yes"])

        submit_single = st.form_submit_button("🚀 Score Lead")

    if submit_single:
        lead_data = {
            "TotalVisits": total_visits,
            "Total Time Spent on Website": time_spent,
            "Page Views Per Visit": pages_per_visit,
            "Last Activity": last_activity,
            "Last Notable Activity": last_activity,
            "What is your current occupation": occupation,
            "Specialization": specialization,
            "Do Not Call": do_not_call,
            "Do Not Email": do_not_email
        }

        with st.spinner("Analyzing lead..."):
            result = asyncio.run(
                graph.ainvoke({
                    "lead_id": 0,
                    "raw_data": lead_data
                })
            )

        render_lead_card("Single Lead Result", result)

# =========================================================
# TAB 2 — BATCH CSV SCORING
# =========================================================
with tab2:
    st.subheader("Upload CSV for Batch Scoring")

    uploaded_file = st.file_uploader("Upload Lead CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(), use_container_width=True)

        if st.button("⚡ Run Batch Scoring"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            results = []
            total_rows = len(df)

            for i, row in df.iterrows():
                status_text.text(f"Processing lead {i+1} of {total_rows}")

                raw_data = row.to_dict()

                result = asyncio.run(
                    graph.ainvoke({
                        "lead_id": i,
                        "raw_data": raw_data
                    })
                )

                results.append({
                    **raw_data,
                    **result
                })

                progress_bar.progress((i + 1) / total_rows)
                time.sleep(1.0)  # Gemini rate-limit safety

            status_text.text("Batch scoring completed")
            st.success("Batch scoring completed!")

            result_df = pd.DataFrame(results)

            # -------- Summary --------
            st.subheader("📊 Results Summary")
            summary_cols = [
                "tier", "final_score", "rule_score", "ml_score",
                "What is your current occupation", "Specialization"
            ]
            summary_cols = [c for c in summary_cols if c in result_df.columns]
            st.dataframe(result_df[summary_cols], use_container_width=True)

            # -------- Cards --------
            st.subheader("🗂 Lead-wise Explanations")
            for idx, row in result_df.iterrows():
                render_lead_card(f"Lead #{idx + 1}", row)

            # -------- Download --------
            st.download_button(
                "⬇️ Download Full Report (with Explanations)",
                data=result_df.to_csv(index=False),
                file_name="scored_leads_full.csv",
                mime="text/csv"
            )
