# threat_intel.py
import requests
import os
from dotenv import load_dotenv
load_dotenv()

OTX_API_KEY = os.getenv("OTX_API_KEY")
HEADERS = {
    "X-OTX-API-KEY": OTX_API_KEY
}

def get_recent_public_pulses(limit=5):
    url = f"https://otx.alienvault.com/api/v1/pulses/explore?limit={limit}"
    headers = {"X-OTX-API-KEY": os.getenv("OTX_API_KEY")}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"[!] Failed to fetch public pulses: {e}")
        return []


def enrich_threat_data(threat):
    # Extract IOCs from threat text
    iocs = extract_iocs(threat['text'])
    
   
def extract_iocs(text):
    # Simplified IOC extraction (in practice, use regex/ML models)
    iocs = []
    # Add domain/IP/CVE extraction logic here
    return iocs