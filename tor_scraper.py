# tor_scraper.py
# Scraps the Darkweb for threats
import requests
import os
from stem import Signal
#Stem allows programs to interact with Tor
from stem.control import Controller
import time

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }
    return session

def renew_tor_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=os.getenv('TOR_PASSWORD'))
        controller.signal(Signal.NEWNYM)
        time.sleep(5)

def scrape_darkweb_forum(url):
    session = get_tor_session()
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Tor request failed: {e}")
        renew_tor_connection()
        return None