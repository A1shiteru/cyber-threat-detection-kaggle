# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import joblib
import requests

# Load trained model and vectorizer
vectorizer = joblib.load('improved_vectorizer.joblib')
classifier = joblib.load('improved_classifier.joblib')

# Sample threat feed endpoint (replace with a real API or DB connection)
THREAT_FEED_URL = "https://example.com/api/threats"  # <-- Replace with real URL

# Authentication credentials (placeholder)
USERNAME = st.secrets.get("username", "admin")
PASSWORD = st.secrets.get("password", "password")

def authenticate():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
        else:
            st.sidebar.error("Invalid credentials")

# Sample data loader - replace with real feed or DB connection
def load_data():
    try:
        response = requests.get(THREAT_FEED_URL)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except:
        # Fallback: use demo data
        return pd.DataFrame({
            'source': ['twitter', 'reddit', 'forum'],
            'text': ['Phishing attack detected', 'New ransomware variant', 'Zero-day vulnerability'],
            'threat_class': ['critical', 'high', 'medium'],
            'confidence': [0.92, 0.85, 0.65],
            'timestamp': [datetime.now() - timedelta(hours=h) for h in [1, 3, 5]]
        })

def predict_threat(text_series):
    X_vec = vectorizer.transform(text_series)
    return classifier.predict(X_vec)

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        authenticate()
        return

    st.title("Cyber Threat Intelligence Dashboard")

    # Load data
    threat_data = load_data()
    threat_data['timestamp'] = pd.to_datetime(threat_data['timestamp'])
    threat_data['end_time'] = threat_data['timestamp'] + pd.Timedelta(hours=1)

    # Predict threat (1 = potential threat, 0 = benign)
    threat_data['predicted_threat'] = predict_threat(threat_data['text'])

    # Threat class ordering
    threat_data['threat_class'] = pd.Categorical(
        threat_data['threat_class'], 
        categories=['critical', 'high', 'medium'], 
        ordered=True
    )

    # Filter
    st.sidebar.header("Filters")
    threat_levels = st.sidebar.multiselect(
        "Filter by Threat Class", 
        options=threat_data['threat_class'].unique(), 
        default=threat_data['threat_class'].unique()
    )
    filtered_data = threat_data[threat_data['threat_class'].isin(threat_levels)]

    # Threat summary
    st.subheader("Threat Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Threats", len(filtered_data))
    col2.metric("Critical Threats", len(filtered_data[filtered_data['threat_class'] == 'critical']))
    col3.metric("Detection Confidence", f"{filtered_data['confidence'].mean():.0%}")

    # Threat timeline
    st.subheader("Threat Timeline")
    fig = px.timeline(
        filtered_data,
        x_start='timestamp',
        x_end='end_time',
        y='source',
        color='threat_class',
        hover_data=['text']
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)

    # Threat details with prediction
    st.subheader("Threat Details")
    filtered_data['timestamp'] = filtered_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    st.dataframe(filtered_data[['source', 'text', 'threat_class', 'confidence', 'timestamp', 'predicted_threat']])

    # Export data
    st.download_button(
        "Download CSV", 
        data=filtered_data.to_csv(index=False), 
        file_name="threats.csv", 
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
