# data_processor.py - Cleans and extracts entities from text data
import spacy
import re
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # Remove URLs, special characters
    text = re.sub(r'http\S+|@\S+|[^A-Za-z0-9\s]+', '', text)
    return text.lower().strip()

def extract_entities(text):
    doc = nlp(text)
    entities = {
        "orgs": [],
        "tech": [],
        "threats": []
    }
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            entities["orgs"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["tech"].append(ent.text)
    
    # Simple threat keyword matching
    threat_keywords = ["phish", "ransom", "malware", "exploit", "breach"]
    for word in text.split():
        if word in threat_keywords:
            entities["threats"].append(word)
            
    return entities

def process_data(raw_data):
    processed = []
    for item in raw_data:
        clean_text = preprocess_text(item['text'])
        entities = extract_entities(clean_text)
        
        processed.append({
            **item,
            "clean_text": clean_text,
            "entities": entities,
            "processed_at": datetime.now().isoformat()
        })
    return processed