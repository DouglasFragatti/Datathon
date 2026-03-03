import pytest
import os
import pandas as pd
from src.train import train_model

def list_to_excel(tmp_path):
    data = {
        'IAA': [8.5, 7.0, 9.0, 10.0, 5.0, 6.0],
        'IEG': [7.0, 6.0, 8.0, 9.0, 4.0, 5.0],
        'IPS': [7.5, 6.5, 8.5, 9.5, 4.5, 5.5],
        'IDA': [6.0, 6.0, 8.0, 9.0, 4.0, 5.0],
        'Matem': [8.0, 7.0, 9.0, 10.0, 5.0, 6.0],
        'Portug': [7.5, 6.5, 8.5, 9.5, 4.5, 5.5],
        'Inglês': [9.0, 8.0, 10.0, 10.0, 6.0, 7.0],
        'IPV': [7.5, 6.5, 8.5, 9.5, 4.5, 5.5],
        'IAN': [8.0, 7.0, 9.0, 10.0, 5.0, 6.0],
        'Fase ideal': ['Fase 2', 'Fase 1', 'Fase 3', 'Fase 4', 'Fase 1', 'Fase 2'],
        'Destaque IEG': ['Não', 'Sim', 'Sim', 'Sim', 'Não', 'Não'],
        'Destaque IDA': ['Não', 'Não', 'Sim', 'Sim', 'Não', 'Não'],
        'Destaque IPV': ['Não', 'Sim', 'Não', 'Sim', 'Não', 'Não'],
        'Defas': [0, 1, -1, 0, 1, 1] 
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "dummy_data.xlsx"
    df.to_excel(file_path, index=False)
    return str(file_path)

def test_train_model(tmp_path):
    # Prepare dummy data file
    data_path = list_to_excel(tmp_path)
    
    # Prepare dummy output path
    model_path = str(tmp_path / "model.pkl")
    
    # Execute the training pipeline
    train_model(data_path, model_path)
    
    # Assert model was trained and saved correctly
    assert os.path.exists(model_path)
