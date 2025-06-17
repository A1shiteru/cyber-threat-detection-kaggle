# threat_detector.py - 
#  identifies and classifies potential cyber threats within textual data using machine learning.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
import os

# Define file paths for model artifacts
VECTORIZER_PATH = "vectorizer.joblib"
CLASSIFIER_PATH = "threat_classifier.joblib"

# Global variables to hold the loaded model and vectorizer
# These will be loaded once when the module is initialized (or first accessed)
vectorizer_model = None
classifier_model = None

def train_and_save_model(train_texts, train_labels):
    """
    Trains the TF-IDF Vectorizer and RandomForestClassifier,
    then saves them to disk. This function should be called explicitly
    when you need to train or retrain your model, NOT every time the script runs.
    """
    print("Training TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train = vectorizer.fit_transform(train_texts)

    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(random_state=42) # Added random_state for reproducibility
    clf.fit(X_train, train_labels)

    # Save model artifacts
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(clf, CLASSIFIER_PATH)
    print(f"Model artifacts saved: {VECTORIZER_PATH}, {CLASSIFIER_PATH}")

def load_model_artifacts():
    """
    Loads the TF-IDF Vectorizer and RandomForestClassifier from disk.
    This function should be called once when the application starts or
    when the module is first used.
    """
    global vectorizer_model, classifier_model # Declare intent to modify global variables
    
    if vectorizer_model is None or classifier_model is None:
        if not os.path.exists(VECTORIZER_PATH) or not os.path.exists(CLASSIFIER_PATH):
            # If models don't exist, we can't load them.
            # In a real scenario, you might want to automatically train if not found,
            # or raise a more specific error.
            print("WARNING: Model artifacts not found. Please train the model first.")
            print("Running a quick training with sample data for demonstration.")
            # Sample training data - Replace with real labeled data
            sample_train_texts = [
                "New phishing campaign targeting bank customers",
                "Critical zero-day in Apache Log4j library",
                "Ransomware group demands 5 million in Bitcoin",
                "Security conference starts next week in Vegas",
                "New firewall version released with security patches",
                "Detecting malicious emails with advanced machine learning",
                "Vulnerability found in popular web server software"
            ]
            sample_train_labels = [1, 1, 1, 0, 0, 1, 1] # 1=threat, 0=benign
            train_and_save_model(sample_train_texts, sample_train_labels)
            
        try:
            print("Loading model artifacts...")
            vectorizer_model = joblib.load(VECTORIZER_PATH)
            classifier_model = joblib.load(CLASSIFIER_PATH)
            print("Model artifacts loaded successfully.")
        except Exception as e:
            print(f"ERROR: Could not load model artifacts: {e}")
            vectorizer_model = None
            classifier_model = None # Ensure they are None if loading fails

def predict_threat(text):
    """
    Predicts if a given text is a threat using the loaded models.
    Assumes load_model_artifacts() has been called.

    Args:
        text (str): The clean text to classify.

    Returns:
        dict: Contains 'is_threat' (boolean), 'confidence' (float),
              and 'threat_class' (str).
    """
    # Ensure models are loaded before prediction
    if vectorizer_model is None or classifier_model is None:
        load_model_artifacts() # Attempt to load if not already loaded

    if vectorizer_model is None or classifier_model is None:
        # If models still can't be loaded, return a default/error state
        print("ERROR: Models not available for prediction. Returning default.")
        return {
            "is_threat": False,
            "confidence": 0.0,
            "threat_class": "unknown"
        }

    X = vectorizer_model.transform([text])
    # clf.predict_proba returns probabilities for all classes.
    # proba[0] gives probabilities for the first sample.
    # For binary classification (0 or 1), proba[0][1] is prob of class 1 (threat).
    proba = classifier_model.predict_proba(X)[0]
    
    # Get the predicted class (0 or 1)
    predicted_class = classifier_model.predict(X)[0]

    return {
        "is_threat": bool(predicted_class), # Convert 0/1 to boolean
        "confidence": float(proba[predicted_class]), # Confidence in the predicted class
        "threat_class": "critical" if proba[1] > 0.7 else "suspicious" if proba[1] > 0.5 else "benign"
    }

def analyze_data(processed_data):
    """
    Applies the threat prediction to a list of processed data items.

    Args:
        processed_data (list of dict): Data processed by data_processor.py.

    Returns:
        list of dict: Each item enriched with 'is_threat', 'confidence', and 'threat_class'.
    """
    # Ensure models are loaded when analyze_data is called from main.py
    load_model_artifacts() 

    results = []
    for item in processed_data:
        # Pass the clean text for prediction
        prediction = predict_threat(item.get("clean_text", "")) # Use .get for safety
        results.append({**item, **prediction})
    return results

if __name__ == "__main__":
    # --- This block is for training the model manually ---
    # Only run this part if you want to (re)train your model.
    # Comment this out after you've trained and saved your models once.
    print("--- Running Model Training Block ---")
    train_texts = [
        "New phishing campaign targeting bank customers",
        "Critical zero-day in Apache Log4j library",
        "Ransomware group demands 5 million in Bitcoin",
        "Security conference starts next week in Vegas",
        "New firewall version released with security patches",
        "Detecting malicious emails with advanced machine learning",
        "Vulnerability found in popular web server software",
        "Upcoming webinar on cloud security best practices",
        "Discussion on quantum computing trends",
        "Team building event next friday"
    ]
    train_labels = [1, 1, 1, 0, 0, 1, 1, 0, 0, 0] # 1=threat, 0=benign
    
    # Call the training function
    train_and_save_model(train_texts, train_labels)
    print("\nModel training/saving complete.")

    # --- This block is for testing prediction using the saved models ---
    print("\n--- Running Prediction Test Block ---")
    # Make sure models are loaded before running tests
    load_model_artifacts()

    sample_texts_for_prediction = [
        "Major data breach reported by a tech giant.",
        "New software update available.",
        "Warning about a new malware variant circulating.",
        "Invitation for an online webinar on AI.",
        "Company XYZ hit by a sophisticated ransomware attack."
    ]

    for text_to_predict in sample_texts_for_prediction:
        prediction_result = predict_threat(text_to_predict)
        print(f"Text: '{text_to_predict}'")
        print(f"  Prediction: {prediction_result['is_threat']}, Confidence: {prediction_result['confidence']:.2f}, Class: {prediction_result['threat_class']}")
        print("-" * 30)

