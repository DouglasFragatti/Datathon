from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

router = APIRouter()

# Load Model
MODEL_PATH = "app/model/model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class StudentData(BaseModel):
    IAA: float
    IEG: float
    IPS: float
    IDA: float
    Matem: float
    Portug: float
    Inglês: float
    IPV: float
    IAN: float
    Fase_ideal: str
    Destaque_IEG: str
    Destaque_IDA: str
    Destaque_IPV: str
    
    # Map Pydantic fields to DataFrame columns (handling spaces)
    def to_df(self):
        data = {
            'IAA': [self.IAA],
            'IEG': [self.IEG],
            'IPS': [self.IPS],
            'IDA': [self.IDA],
            'Matem': [self.Matem],
            'Portug': [self.Portug],
            'Inglês': [self.Inglês],
            'IPV': [self.IPV],
            'IAN': [self.IAN],
            'Fase ideal': [self.Fase_ideal],
            'Destaque IEG': [self.Destaque_IEG],
            'Destaque IDA': [self.Destaque_IDA],
            'Destaque IPV': [self.Destaque_IPV]
        }
        return pd.DataFrame(data)

import logging
import json
from datetime import datetime

# Setup Logger
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/predictions.jsonl",
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger("drift_monitor")

@router.post("/predict")
def predict(data: StudentData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        df = data.to_df()
        prediction = model.predict(df)[0]
        # prediction is likely a string or int (e.g. -1, 0)
        
        # Calculate crude probability (highest prob)
        probs = model.predict_proba(df)[0]
        max_prob = max(probs)
        
        result = {
            "prediction": str(prediction),
            "confidence": float(max_prob),
            "label_description": "Defasagem score (0=OnTrack, <0=Advanced?, >0=Lag)" 
        }
        
        # Log for Drift Monitoring
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "inputs": data.dict(),
            "output": result
        }
        logger.info(json.dumps(log_entry))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
