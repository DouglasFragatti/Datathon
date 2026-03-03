import pytest
import numpy as np
from src.evaluate import evaluate_model

def test_evaluate_model(capsys):
    y_true = np.array(['0', '1', '0', '1', '2'])
    y_pred = np.array(['0', '1', '0', '0', '2'])
    
    # We call evaluate_model and expect it to print metrics to stdout.
    evaluate_model(y_true, y_pred)
    
    # Capture print outputs to verify it ran correctly
    captured = capsys.readouterr()
    
    assert "--- Classification Report ---" in captured.out
    assert "Accuracy:" in captured.out
    assert "--- Confusion Matrix ---" in captured.out
