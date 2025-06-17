# db_handler.py
import json
import psycopg2
from psycopg2 import sql
import os

def create_threats_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS threats (
            id SERIAL PRIMARY KEY,
            raw_text TEXT,
            clean_text TEXT,
            source VARCHAR(50),
            entities JSONB,
            is_threat BOOLEAN,
            threat_class VARCHAR(20),
            confidence FLOAT,
            url TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def save_threats(threats):
    conn = get_db_connection()
    cur = conn.cursor()
    for threat in threats:
        cur.execute(
            """
            INSERT INTO threats (
                raw_text, clean_text, source, entities, 
                is_threat, threat_class, confidence, url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                threat.get('text'),
                threat.get('clean_text'),
                threat.get('source'),
                json.dumps(threat.get('entities')),
                threat.get('is_threat'),
                threat.get('threat_class'),
                threat.get('confidence'),
                threat.get('url')
            )
        )
    conn.commit()
    cur.close()
    conn.close()

def load_threats(limit=100):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM threats ORDER BY timestamp DESC LIMIT %s", (limit,))
    columns = [desc[0] for desc in cur.description]
    results = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results