# siem_integration.py - Sends threat data to SIEM (e.g., Splunk)
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")

if not SPLUNK_URL or not SPLUNK_TOKEN:
    raise ValueError("SPLUNK_URL and SPLUNK_TOKEN must be set in your .env")


def send_to_splunk(threat, index="threat_intel"):
    url = f"{SPLUNK_URL}/services/collector/event"

    headers = {
        "Authorization": f"Splunk {os.getenv('SPLUNK_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "event": threat,
        "index": index,
        "sourcetype": "_json"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error sending to Splunk: {e}")
        return False