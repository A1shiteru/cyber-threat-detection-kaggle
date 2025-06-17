# feedback_system.py
import psycopg2
import joblib
import os
import numpy as np

def get_db_connection():
    # Update these parameters with your actual database credentials
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_db_user",
        password="your_db_password",
        host="localhost",
        port="5432"
    )

def update_model_with_feedback():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM threats WHERE feedback IS NOT NULL")
    feedback_data = cur.fetchall()
    
    if not feedback_data:
        return
    
    vectorizer = joblib.load('improved_vectorizer.joblib')
    model = joblib.load('improved_classifier.joblib')
    
    X = []
    y = []
    
    for row in feedback_data:
        X.append(row['clean_text'])
        y.append(1 if row['feedback'] == 'confirmed' else 0)
    
    if not X:
        return
    
    X_vec = vectorizer.transform(X)
    
    # Partial fit with new data
    model.partial_fit(X_vec, np.array(y), classes=[0, 1])
    
    # Save updated model
    joblib.dump(model, 'improved_classifier.joblib')
    
    # Clear feedback
    cur.execute("UPDATE threats SET feedback = NULL WHERE feedback IS NOT NULL")
    conn.commit()
    cur.close()
    conn.close()