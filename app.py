import streamlit as st
import pandas as pd
import json
from utils.extractor import extract_text
from utils.preprocessor import get_clauses
from logic import get_legal_analysis, identify_language

# 1. PAGE SETUP
st.set_page_config(page_title="LegalShield AI | Enterprise", page_icon="🏛️", layout="wide")

# FIX: Force load Material Icons for hosted environments
st.markdown('<link href="[https://fonts.googleapis.com/icon?family=Material+Icons](https://fonts.googleapis.com/icon?family=Material+Icons)" rel="stylesheet">', unsafe_allow_html=True)

# CUSTOM CSS: Enterprise Metrics
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 15px 10px;
        border-radius: 10px;
        border: 1px solid #2d3139;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    div[data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #9ca3af !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { font-size: 1.2rem !important; font-weight: 600 !important; white-space: normal !important; word-break: break-word !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR - Corporate Branding
with st.sidebar:
    st.markdown("## 🏛️ LegalShield AI")
    st.caption("Secure Enterprise Edition")
    st.divider()
    st.info("Status: System Ready")
    st.divider()
    st.markdown("### Compliance Standards")
    st.caption("✔️ Indian Contract Act 1872")
    st.caption("✔️ SME Data Protection Protocol")
    st.divider()
    st.caption("© 2026 SME Legal Intelligence")

# 3. MAIN INTERFACE
st.title("🏛️ Contract Intelligence Platform")
st.markdown("Automated risk assessment and entity extraction for Indian SMEs.")

uploaded_file = st.file_uploader("Upload Legal Document (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])

if uploaded_file:
    with st.status("🔍 Deep Document Audit in Progress...", expanded=False) as status:
        raw_text = extract_text(uploaded_file)
        lang = identify_language(raw_text[:500])
        clauses = get_clauses(raw_text)
        analysis = get_legal_analysis(clauses)
        status.update(label="Audit Complete", state="complete")

    if "error" not in analysis:
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        score = analysis['composite_score']
        m1.metric("Risk Index", f"{score}/100", "SECURE" if score < 40 else "CRITICAL", delta_color="inverse")
        m2.metric("Category", analysis['contract_type'])
        m3.metric("Language", "Hindi" if lang == "hi" else "English")
        m4.metric("Entities Found", len(analysis['entities'].get('parties', [])))

        st.divider()
        st.subheader("🔍 Clause-by-Clause Audit")
        tab_prio, tab_full = st.tabs(["⚠️ Priority Risks", "📋 Full Audit Table"])
        with tab_prio:
            priority = [i for i in analysis['analysis'] if i['risk_level'] in ["High", "Medium"]]
            if priority:
                for item in priority:
                    with st.expander(f"⚠️ {item['clause_type'].upper()} — {item['risk_level']}"):
                        st.write(f"**Legal Issue:** {item['explanation']}")
                        st.success(f"**SME Strategy:** {item['renegotiation']}")
            else: st.success("No high-priority risks detected.")
        with tab_full: st.dataframe(analysis['analysis'], use_container_width=True)

        st.divider()
        # Side-by-Side Dashboard
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("📊 Compliance Radar")
            bench = analysis.get('benchmarks', {"liability": 50, "termination": 50, "payment": 50, "ip_rights": 50})
            chart_data = pd.DataFrame(bench.items(), columns=["Metric", "Score"])
            st.bar_chart(chart_data, x="Metric", y="Score")
        with col_right:
            st.subheader("📖 Executive Summary")
            with st.container(border=True):
                st.info(analysis['summary'])
                st.markdown("---")
                ent = analysis.get('entities', {})
                st.write(f"**Parties:** {', '.join(ent.get('parties', ['N/A']))}")
                st.write(f"**Jurisdiction:** {ent.get('jurisdiction', 'N/A')}")
                st.write(f"**Financial Value:** {ent.get('total_value', 'N/A')}")
                st.download_button("📥 Export Audit Log (JSON)", str(analysis), "audit_trail.json", use_container_width=True)
