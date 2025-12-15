import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from src.preprocessing import get_preprocessor
from src.feature_engineering import FeatureEngineer
from src.evaluate import evaluate_model

def train_model(data_path: str, model_path: str):
    print(f"Loading data from {data_path}...")
    df = pd.read_excel(data_path)
    
    # Target
    target_col = 'Defas'
    if target_col not in df.columns:
        raise ValueError(f"Target column {target_col} not found!")

    # Binarize/Process Target for simpler 'Risk' prediction if desired?
    # For now, let's try to predict the raw class.
    # But wait, -1, -2 etc might be better as mapped classes.
    # Map: <0 -> 'Advanced/OnTrack', >=0 -> 'Risk'? 
    # Based on distribution, 0 is very common.
    # Let's keep it as is, or maybe string classes. 
    # To correspond to 'Risk', we'll just train the classifier.
    
    X = df.drop(columns=[target_col])
    y = df[target_col].astype(str) # Treat as categorical
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Initializing pipeline...")
    pipeline = Pipeline(steps=[
        ('feature_engineering', FeatureEngineer()),
        ('preprocessor', get_preprocessor()),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test) # Complex for multiclass ROC, handle in evaluate
    
    evaluate_model(y_test, y_pred)
    
    print(f"Saving model to {model_path}...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    print("Done.")

if __name__ == "__main__":
    DATA_FILE = r"c:\Projetos\Tech5\data\BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
    MODEL_FILE = r"c:\Projetos\Tech5\app\model\model.pkl"
    train_model(DATA_FILE, MODEL_FILE)
