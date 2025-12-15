import requests
import json
import random

url = "http://127.0.0.1:8000/predict"

# Base payload
payload = {
  "IAA": 8.5, "IEG": 7.2, "IPS": 7.5, "IDA": 6.8, "Matem": 6.0,
  "Portug": 7.5, "Inglês": 8.0, "IPV": 7.9, "IAN": 6.5,
  "Fase_ideal": "Fase 2",
  "Destaque_IEG": "Seu destaque", "Destaque_IDA": "Ponto de melhoria", "Destaque_IPV": "Seu destaque"
}

print("Sending 5 requests to generate logs...")
for _ in range(5):
    # Add random noise to inputs
    mod_payload = payload.copy()
    mod_payload['IAA'] += random.uniform(-1, 1)
    
    try:
        resp = requests.post(url, json=mod_payload)
        print(f"Status: {resp.status_code}, Pred: {resp.json().get('prediction')}")
    except Exception as e:
        print(f"Request failed: {e}")
