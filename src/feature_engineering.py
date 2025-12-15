import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        # Ensure numeric columns exist before mean
        cols = ['Portug', 'Matem', 'Inglês']
        existing_cols = [c for c in cols if c in X.columns]
        
        if existing_cols:
            X['Média_Geral'] = X[existing_cols].mean(axis=1)
        
        return X
