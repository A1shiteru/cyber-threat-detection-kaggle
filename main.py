# main.py
from data_collector import get_rss_threats,get_darkweb_samples
from data_processor import process_data
from threat_detector import analyze_data
from alert_system import monitor_threats

def run_pipeline():
    # Collect data
    raw_data = []

# Add RSS
    from data_collector import get_rss_threats
    rss_feeds = ["https://threatpost.com/feed/", "https://www.us-cert.gov/ncas/alerts.xml"]
    raw_data.extend(get_rss_threats(rss_feeds))

      # Add MISP
    #from data_collector import get_misp_threats
    #raw_data.extend(get_misp_threats())

    
    raw_data.extend(get_darkweb_samples())
    
    # Process data
    processed = process_data(raw_data)
    
    # Analyze threats
    analyzed = analyze_data(processed)
    
    # Alert on critical threats
    monitor_threats(analyzed)
    
    return analyzed

if __name__ == "__main__":
    threats = run_pipeline()
    print(f"Processed {len(threats)} items, found {sum(t['is_threat'] for t in threats)} threats")
    