import spacy

# Load the model directly installed from requirements.txt
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback for local development environments
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def get_clauses(text):
    doc = nlp(text)
    # Filter for significant clauses
    clauses = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
    return clauses