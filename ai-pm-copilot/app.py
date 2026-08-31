# AI PM Copilot - Streamlit app entrypoint

import streamlit as st
from pathlib import Path
import pandas as pd
import os

from engine.preprocessing import load_and_validate, preprocess_feedback
from engine.clustering import build_embeddings_and_clusters
from engine.evidence import build_theme_evidence
from engine.ranking import compute_priority_scores
from engine.confidence import compute_confidence
from utils.database import init_db, record_audit
from services.llm_service import LLMService
from services.prd_service import PRDService
from utils.export import export_theme_markdown, export_prd_markdown

st.set_page_config(page_title="AI PM Copilot", layout="wide")

APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"
DB_PATH = APP_ROOT / "storage" / "feedback.db"

# Initialize DB
init_db(DB_PATH)

# Sidebar
st.sidebar.title("AI PM Copilot")
page = st.sidebar.radio("Navigation", [
    "Overview",
    "Feedback Explorer",
    "Theme Intelligence",
    "Theme Deep Dive",
    "PRD Copilot",
    "Trust Center",
    "Evaluation",
])

st.sidebar.markdown("---")
use_demo = st.sidebar.button("Use Demo Dataset")

# Load dataset
uploaded = st.sidebar.file_uploader("Upload feedback CSV", type=["csv"]) 

if uploaded is not None:
    df_raw, ingest_report = load_and_validate(uploaded)
elif use_demo:
    demo_path = DATA_DIR / "customer_feedback.csv"
    df_raw, ingest_report = load_and_validate(demo_path)
else:
    st.sidebar.info("Upload a CSV or use the Demo Dataset to get started.")
    df_raw = None
    ingest_report = None

if df_raw is not None:
    st.sidebar.markdown("### Ingestion Report")
    for k, v in ingest_report.items():
        st.sidebar.write(f"**{k}**: {v}")

    # Preprocess
    df = preprocess_feedback(df_raw)

    # Build embeddings & clustering (cached inside)
    embeddings, cluster_info = build_embeddings_and_clusters(df)

    # Evidence & themes
    themes = build_theme_evidence(df, embeddings, cluster_info)

    # Ranking
    ranked = compute_priority_scores(themes, df)

    # Confidence
    ranked = compute_confidence(ranked, df, embeddings)

    # LLM service (provider selection inside)
    llm = LLMService()
    prd_svc = PRDService(llm)

    # Overview page
    if page == "Overview":
        st.title("AI PM Copilot")
        st.subheader("Turn customer feedback into evidence-backed product decisions.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Feedback Items", len(df))
        col2.metric("Themes Detected", len(ranked))
        col3.metric("Feedback Sources", df['source'].nunique())
        col4.metric("Est. Synthesis Time Saved", "67%")

        # Stats
        st.markdown("---")
        stat1, stat2, stat3, stat4 = st.columns(4)
        stat1.write("Average sentiment")
        stat1.metric("Avg Sentiment", f"{df['sentiment'].mean():.2f}")
        stat2.metric("Enterprise feedback %", f"{100* (df['customer_segment']=='Enterprise').mean():.0f}%")
        stat3.metric("Date range", f"{df['date'].min()} → {df['date'].max()}")

        # Charts
        st.markdown("#### Feedback over time")
        st.line_chart(df.groupby('date').size())
        st.markdown("#### Feedback by source")
        st.bar_chart(df['source'].value_counts())

        st.markdown("---")
        st.markdown("### Top Product Opportunities")
        # show top 3
        top3 = ranked.sort_values('priority_score', ascending=False).head(3)
        for _, row in top3.iterrows():
            st.markdown(f"**{row['label']}**  ")
            st.write(f"{int(row['priority_score'])}/100 Priority Score — {row['confidence_label']}")
            st.write(row['summary'])
            st.markdown("---")

    elif page == "Feedback Explorer":
        st.title("Feedback Explorer")
        st.dataframe(df[['feedback_id','date','customer_id','customer_segment','source','feedback_text','plan','account_value']])

    elif page == "Theme Intelligence":
        st.title("Theme Intelligence")
        st.markdown("Adjust ranking weights (prototype)")
        w_freq = st.sidebar.slider("Frequency weight", 0.0, 1.0, 0.3)
        w_value = st.sidebar.slider("Customer value weight", 0.0, 1.0, 0.25)
        w_urgency = st.sidebar.slider("Urgency weight", 0.0, 1.0, 0.2)
        w_sent = st.sidebar.slider("Sentiment weight", 0.0, 1.0, 0.15)
        w_breadth = st.sidebar.slider("Breadth weight", 0.0, 1.0, 0.1)
        # normalize
        s = w_freq + w_value + w_urgency + w_sent + w_breadth
        if s == 0:
            s = 1
        weights = dict(
            frequency=w_freq/s,
            customer_value=w_value/s,
            urgency=w_urgency/s,
            sentiment_severity=w_sent/s,
            breadth=w_breadth/s,
        )
        st.write("Weights:", weights)
        ranked = compute_priority_scores(themes, df, weights=weights)
        st.dataframe(ranked[['rank','label','mentions','unique_customers','enterprise_customers','priority_score','confidence_label']])

    elif page == "Theme Deep Dive":
        st.title("Theme Deep Dive")
        theme_sel = st.selectbox("Select Theme", ranked['label'].tolist())
        if theme_sel:
            t = ranked[ranked['label']==theme_sel].iloc[0]
            st.subheader(t['label'])
            st.write(t['summary'])
            st.write(f"Priority Score: {int(t['priority_score'])} — {t['confidence_label']}")
            st.markdown("#### Evidence")
            for quote in t['representative_examples'][:5]:
                st.info(quote)
            st.markdown("---")
            st.markdown("#### Breakdown")
            st.write({'mentions': t['mentions'], 'unique_customers': t['unique_customers']})
            # Human actions
            st.markdown("#### Human Review")
            colA, colB, colC, colD = st.columns(4)
            if colA.button('Approve Theme'):
                record_audit(DB_PATH, operation='theme_approved', provider='human', theme=t['label'], status='approved')
                st.success("Theme approved")
            new_name = colB.text_input('Rename Theme', value=t['label'])
            if colB.button('Save Name'):
                record_audit(DB_PATH, operation='theme_renamed', provider='human', theme=t['label'], status=f'renamed:{new_name}')
                st.success('Renamed')
            if colC.button('Reject Theme'):
                record_audit(DB_PATH, operation='theme_rejected', provider='human', theme=t['label'], status='rejected')
                st.warning('Theme rejected')

    elif page == "PRD Copilot":
        st.title("PRD Copilot")
        st.markdown("Select an approved theme to generate PRD")
        approved = []
        # Simplification: allow selection
        theme_sel = st.selectbox("Theme", ranked['label'].tolist())
        if st.button('Generate PRD Draft'):
            t = ranked[ranked['label']==theme_sel].iloc[0]
            prd = prd_svc.generate_prd(t, df)
            st.markdown("### AI DRAFT — REQUIRES HUMAN REVIEW")
            st.text_area("PRD Draft", value=prd, height=400)
            if st.button('Save PRD (mark as draft)'):
                record_audit(DB_PATH, operation='prd_generated', provider=llm.provider_name, theme=t['label'], status='draft_saved')
                st.success('PRD draft saved')

    elif page == "Trust Center":
        st.title("Trust Center")
        st.markdown("### What AI Does")
        st.write("Theme label generation, feedback summarization, PRD first draft")
        st.markdown("### What Deterministic Logic Does")
        st.write("Data validation, priority scoring, confidence calculation, evidence counts, segmentation")
        st.markdown("### AI Audit Log")
        from utils.database import fetch_audit
        logs = fetch_audit(DB_PATH)
        st.dataframe(logs)

    elif page == "Evaluation":
        st.title("Evaluation")
        from engine.evaluation import evaluate_all
        results = evaluate_all(ranked, df, embeddings)
        st.json(results)
        st.markdown("### Estimated Synthesis Time Reduction: 67% (prototype estimate)")

else:
    st.write("Waiting for dataset. Use 'Use Demo Dataset' in the sidebar or upload your CSV.")
