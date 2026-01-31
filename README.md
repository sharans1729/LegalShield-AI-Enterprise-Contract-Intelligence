# ⚖️ SME Legal Assistant - Data Science Hackathon 2026

An AI-powered legal assistant designed to help small and medium business owners in India understand complex contracts, identify legal risks, and receive actionable advice.

## 🚀 Key Functionalities
- **Contract Risk Scoring:** Clause-by-clause and composite risk assessment.
- **Multilingual Support:** Handles English and Hindi contract parsing.
- **Actionable Insights:** Provides "Plain Language" explanations and renegotiation strategies.
- **Compliance Tracking:** Built-in JSON-based audit trails for every analysis.

## 🛠️ Tooling Stack
- **LLM:** GPT-4o (via GitHub Models)
- **NLP:** Python with spaCy (Preprocessing)
- **UI:** Streamlit
- **Storage:** Local file & JSON-based logs

## 🏃 How to Run
1. `pip install -r requirements.txt`
2. `python -m spacy download en_core_web_sm`
3. `streamlit run app.py`