# data_collector.py
import requests
from bs4 import BeautifulSoup
import os
import feedparser
from dotenv import load_dotenv
from pymisp import ExpandedPyMISP
load_dotenv()

# RSS feeds
def get_rss_threats(feed_urls):
    threats = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            threats.append({
                'source': 'rss',
                'text': entry.get('title', '') + '\n' + entry.get('summary', ''),
                'url': entry.get('link', ''),
                'timestamp': entry.get('published', '')
            })
    return threats

# MISP threats collector / Feeds

#def get_misp_threats():
    misp_url = os.getenv("MISP_URL")
    misp_key = os.getenv("MISP_API_KEY")
    misp_verifycert = False  # Set to True in production with valid SSL

    misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)
    events = misp.search(controller='events', return_format='json', limit=10)
    
    threats = []
    for event in events['response']:
        evt = event['Event']
        threats.append({
            'source': 'misp',
            'text': evt.get('info', ''),
            'url': f"{misp_url}/events/view/{evt['id']}",
            'timestamp': evt.get('date', '')
        })
    return threats


def get_rss_threats(feed_urls):
    threats = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            threats.append({
                'source': 'rss',
                'text': entry.get('title', '') + '\n' + entry.get('summary', ''),
                'url': entry.get('link', ''),
                'timestamp': entry.get('published', '')
            })
    return threats

# Dark Web Collector (Simplified)
def get_darkweb_samples():
    # In production: Use Tor with Stem library
    # For MVP: Simulate with clearnet security forums
    threats = []
    response = requests.get("https://security.stackexchange.com/questions?sort=newest")
    soup = BeautifulSoup(response.text, 'html.parser')

    for question in soup.select('.question-summary')[:20]:
        threats.append({
            'text': question.select_one('.question-hyperlink').text,
            'source': 'security_forum',
            'timestamp': question.select_one('.relativetime')['title'],
            'url': "https://security.stackexchange.com" + question.select_one('.question-hyperlink')['href']
        })
    return threats