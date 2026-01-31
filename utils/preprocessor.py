import spacy
import os

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def get_clauses(text):
    doc = nlp(text)
    clauses = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
    return clauses
