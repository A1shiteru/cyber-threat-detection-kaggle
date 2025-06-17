# secure_dashboard.py
import streamlit as st
import hashlib
import os

# Simple credential storage (use proper secrets management in production)
CREDENTIALS = {
    "analyst": hashlib.sha256(os.getenv('DASHBOARD_PASSWORD').encode()).hexdigest()
}

def login():
    st.sidebar.title("Authentication")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username in CREDENTIALS:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == CREDENTIALS[username]:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid password")
        else:
            st.sidebar.error("User not found")
    return False

def main():
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        if login():
            st.session_state.authenticated = True
        else:
            return
    
    # Your existing dashboard code here
    st.title("Secure Threat Intelligence Dashboard")
    # ... rest of the dashboard

if __name__ == "__main__":
    main()