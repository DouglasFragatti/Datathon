from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import io

def evaluate_model(y_true, y_pred, y_prob=None):
    print("\n--- Classification Report ---")
    print(classification_report(y_true, y_pred))
    
    acc = accuracy_score(y_true, y_pred)
    print(f"\nAccuracy: {acc:.4f}")
    
    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_true, y_pred)
    print(cm)
