# train_merged_model.py
# Model - Classify if content is a threat.

#Assigns a confidence score.

#Labels the threat class (e.g., malware, phishing).
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from data_loader import load_threat_dataset  # Use the new loader
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from data_loader import load_threat_dataset

def train_and_save_model():
    print("\n--- Starting Model Training ---")
    
    df = load_threat_dataset()
    X = df['text']
    y = df['is_threat']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Dataset split: {len(X_train)} training samples, {len(X_test)} test samples.")

    # TF-IDF vectorization (improved)
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 3),
        stop_words='english'
    )
    print("Vectorizing text using TF-IDF (unigrams + bigrams + trigrams)...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"TF-IDF vectorization complete. Feature matrix shape: {X_train_vec.shape}")

    # Train the model (improved with class balancing)
    model = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42)
    print("Training RandomForestClassifier...")
    model.fit(X_train_vec, y_train)
    print("Model training complete.")

    # Evaluate
    predictions = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, predictions)
    print(f"\nModel Accuracy on Test Set: {accuracy:.2f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    # Save model artifacts
    joblib.dump(vectorizer, 'improved_vectorizer.joblib')
    joblib.dump(model, 'improved_classifier.joblib')
    print("\nModel artifacts saved:")
    print("  Vectorizer -> improved_vectorizer.joblib")
    print("  Classifier -> improved_classifier.joblib")
    print("\nModel training pipeline completed successfully.")

    return model

if __name__ == "__main__":
    train_and_save_model()
