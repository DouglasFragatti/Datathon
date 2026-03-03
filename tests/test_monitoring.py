import pytest
import os
import json
import src.monitoring

def test_analyze_drift_no_logs(capsys, tmp_path):
    log_file = tmp_path / "predictions_not_exist.jsonl"
    src.monitoring.LOG_FILE = str(log_file)
    
    src.monitoring.analyze_drift()
    
    captured = capsys.readouterr()
    assert "No logs found. Make some predictions first!" in captured.out

def test_analyze_drift_empty_logs(capsys, tmp_path):
    log_file = tmp_path / "predictions_empty.jsonl"
    log_file.touch()
    src.monitoring.LOG_FILE = str(log_file)
    
    src.monitoring.analyze_drift()
    
    captured = capsys.readouterr()
    assert "Log file is empty." in captured.out

def test_analyze_drift_with_data(capsys, tmp_path):
    log_file = tmp_path / "predictions_with_data.jsonl"
    data1 = {
        "inputs": {"IAA": 8.0, "IEG": 7.0},
        "output": {"prediction": "0", "confidence": 0.95}
    }
    data2 = {
        "inputs": {"IAA": 9.0, "IEG": 8.0},
        "output": {"prediction": "1", "confidence": 0.80}
    }
    with open(log_file, "w") as f:
        f.write(json.dumps(data1) + "\n")
        f.write(json.dumps(data2) + "\n")
        
    src.monitoring.LOG_FILE = str(log_file)
    
    src.monitoring.analyze_drift()
    
    captured = capsys.readouterr()
    assert "Total Predictions: 2" in captured.out
    assert "Prediction Distribution" in captured.out
    assert "Average Confidence" in captured.out
    assert "Input Stats (IAA)" in captured.out
