# alert_system.py

import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ALERT_LOG_FILE = "alerts_log.csv"
ALERT_LIMIT = 5
CONFIDENCE_THRESHOLD = 0.9
ALLOWED_THREAT_CLASSES = []  # Empty list means no filtering — allow all threat types

# Function to send alert emails when a threat is detected
# SMTP will be loaded from environment variables
def send_alert(threat_data):
    # Load SMTP and email config from environment
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    email_from = os.getenv('ALERT_EMAIL_FROM')
    email_to = os.getenv('ALERT_EMAIL_TO')

    # Validate that all required environment variables are set
    if not all([smtp_server, smtp_port, smtp_username, smtp_password, email_from, email_to]):
        raise ValueError("Missing one or more required environment variables. Please check your .env file.")

    # Format the alert message
    msg = MIMEText(
        f" THREAT DETECTED \n\n"
        f"Source: {threat_data['source']}\n"
        f"Confidence: {threat_data['confidence']:.2f}\n"
        f"Threat Type: {threat_data['threat_class'].upper()}\n"
        f"Content Preview: {threat_data['text'][:200]}...\n\n"
        f"View full details: {threat_data['url']}"
    )

    msg['Subject'] = f"[ALERT] {threat_data['threat_class'].upper()} threat detected"
    msg['From'] = email_from
    msg['To'] = email_to

    # Send the email using Gmail's SMTP server
    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"[+] Alert sent successfully to {email_to}")
    except Exception as e:
        print(f"[!] Failed to send alert: {e}")

def monitor_threats(analyzed_data):
    for item in analyzed_data:
        if item.get('is_threat') and item.get('confidence', 0) > 0.7:
            send_alert(item)
