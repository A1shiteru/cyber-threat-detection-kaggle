# data_loader.py
# This module is responsible for loading and initial preprocessing of datasets.

import pandas as pd
import os

def load_threat_dataset(path='Cybersecurity_Dataset.csv'):
    """
    Loads a cyber threat dataset from a CSV file, performs basic preprocessing,
    and structures it for machine learning model training.

    This version is adapted to load the "NLP Based Cyber Security Dataset" from Kaggle.

    Args:
        path (str): The file path to the dataset CSV.
                    Default is 'Cybersecurity_Dataset.csv'.

    Returns:
        pandas.DataFrame: A DataFrame with 'text' and 'is_threat' columns,
                          ready for machine learning model training.
                          Returns an empty DataFrame if the file is not found
                          or required columns are missing.
    """
    if not os.path.exists(path):
        print(f"Error: Dataset file not found at '{path}'. "
              "Please ensure your dataset CSV is in the correct directory.")
        return pd.DataFrame(columns=['text', 'is_threat']) # Return empty DataFrame on error

    print(f"Loading dataset from: {path}")
    df = pd.read_csv(path)
    
    # Define expected columns from the "NLP Based Cyber Security Dataset"
    # IMPORTANT: These must match the exact column names in your CSV file.
    text_column_name = 'Cleaned Threat Description'
    severity_column_name = 'Severity Score'

    # Check for required columns in the loaded DataFrame
    if text_column_name not in df.columns or severity_column_name not in df.columns:
        print(f"Error: Dataset must contain '{text_column_name}' and '{severity_column_name}' columns.")
        print(f"Found columns: {df.columns.tolist()}")
        return pd.DataFrame(columns=['text', 'is_threat'])

    # Map dataset columns to the 'text' and 'is_threat' columns expected by model_trainer.py
    # .astype(str) ensures the text column is treated as strings, and .fillna('') handles any empty cells.
    df['text'] = df[text_column_name].astype(str).fillna('') 
    
    # Convert 'Severity Score' (1-5) to a binary 'is_threat' label (1 or 0).
    # Here, we consider anything with Severity Score GREATER THAN 2 as a threat (1).
    # You can adjust this threshold (e.g., >3, >=3) based on your definition of a "threat".
    df['is_threat'] = df[severity_column_name].apply(lambda x: 1 if x > 2 else 0)
    
    print(f"Dataset loaded with {len(df)} entries.")
    print(f"Threat distribution (is_threat=1 vs 0): {df['is_threat'].value_counts().to_dict()}")
    
    return df[['text', 'is_threat']] # Return only the newly created 'text' and 'is_threat' columns

# Example usage (for testing this module directly)
if __name__ == "__main__":
    # This block is just for testing data_loader.py in isolation.
    # If you have 'Cybersecurity_Dataset.csv' in your project root, it will use that.
    # Otherwise, it creates a small dummy file to allow testing.
    
    test_csv_path = 'Cybersecurity_Dataset.csv' # Pointing to the actual expected dataset name

    # Create a dummy CSV for testing if the actual file doesn't exist
    if not os.path.exists(test_csv_path):
        print(f"Creating a dummy '{test_csv_path}' for isolated testing...")
        dummy_data = {
            'Threat Category': ['Phishing', 'Malware', 'DDoS', 'Benign', 'Ransomware', 'Alert'],
            'Cleaned Threat Description': [
                "phishing email detected targeting internal users",
                "new malware variant spreading rapidly globally",
                "distributed denial of service attack ongoing",
                "weekly security bulletin update for system patches",
                "ransomware group demands payment in bitcoin after encrypting data",
                "low severity alert about a software update"
            ],
            'IOCs': [[], [], [], [], [], []],
            'Threat Actor': ['Unknown', 'APT-X', 'Unknown', 'None', 'DarkGroup', 'None'],
            'Attack Vector': ['Email', 'Network', 'Web', 'None', 'Network', 'Software'],
            'Sentiment in Forums': [0.8, 0.9, 0.7, 0.2, 0.95, 0.3],
            'Severity Score': [4, 5, 3, 1, 5, 2], # Examples: 4,5,3 -> threat; 1,2 -> benign
            'Predicted Threat Category': ['Phishing', 'Malware', 'DDoS', 'Benign', 'Ransomware', 'Benign'],
            'Suggested Defense Mechanism': [],
            'Risk Level Prediction': [4, 5, 3, 1, 5, 2]
        }
        dummy_df = pd.DataFrame(dummy_data)
        dummy_df.to_csv(test_csv_path, index=False)
        print("Dummy dataset created.")

    print("\n--- Testing data_loader.py ---")
    loaded_data = load_threat_dataset(test_csv_path)
    if not loaded_data.empty:
        print("\nLoaded Data Head:")
        print(loaded_data.head())
        print("\nLoaded Data Columns:")
        print(loaded_data.columns.tolist())
    else:
        print("Failed to load data or dataset is empty.")
