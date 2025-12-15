import pandas as pd
import json
import os
import matplotlib.pyplot as plt

LOG_FILE = "logs/predictions.jsonl"

def analyze_drift():
    if not os.path.exists(LOG_FILE):
        print("No logs found. Make some predictions first!")
        return

    print("Loading logs...")
    data = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    
    if not data:
        print("Log file is empty.")
        return

    # Create DataFrame from logs
    df_logs = pd.json_normalize(data)
    print(f"\nTotal Predictions: {len(df_logs)}")
    
    # 1. Prediction Distribution (Target Drift)
    print("\n--- Prediction Distribution (Real-time) ---")
    pred_counts = df_logs['output.prediction'].value_counts(normalize=True)
    print(pred_counts)
    
    # 2. Confidence Drift
    print("\n--- Average Confidence ---")
    print(f"Mean Confidence: {df_logs['output.confidence'].mean():.4f}")

    # 3. Input Drift Example (e.g., Mean of IAA)
    if 'inputs.IAA' in df_logs.columns:
        print("\n--- Input Stats (IAA) ---")
        print(f"Mean IAA: {df_logs['inputs.IAA'].mean():.2f}")

if __name__ == "__main__":
    analyze_drift()
