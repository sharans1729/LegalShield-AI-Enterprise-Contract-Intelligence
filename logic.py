import os
import json
from langdetect import detect
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables for security
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")

def get_legal_analysis(clauses):
    if not GITHUB_TOKEN:
        return {"error": "Authentication Token Missing. Check Secrets."}

    context_text = "\n".join(clauses[:15]) 

    system_prompt = """
    You are a Senior Legal Analyst for Indian SME Law (Contract Act 1872). 
    Perform a deep audit and output strictly in JSON format.
    
    1. ENTITIES: Extract Parties, Dates, Jurisdiction, and Total Financial Liability.
    2. RISK ENGINE: Score risks (1-100) and provide SME-friendly advice.
    3. BENCHMARKS: Evaluate liability, termination, payment, and IP terms (0-100).
    
    JSON Structure:
    {
        "entities": {"parties": [], "dates": [], "jurisdiction": "", "total_value": ""},
        "contract_type": "string",
        "composite_score": int,
        "summary": "plain language summary",
        "benchmarks": {"liability": int, "termination": int, "payment": int, "ip_rights": int},
        "analysis": [
            {"clause_type": "string", "risk_level": "High/Med/Low", "explanation": "string", "renegotiation": "string"}
        ]
    }
    """

    try:
        client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(GITHUB_TOKEN))
        response = client.complete(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this contract:\n{context_text}"}
            ],
            model="gpt-4o"
        )
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}

def identify_language(text):
    try:
        return detect(text) if text.strip() else "en"
    except:
        return "en"
