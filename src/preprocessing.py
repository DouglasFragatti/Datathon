import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.drop(columns=[c for c in self.columns_to_drop if c in X.columns], errors='ignore')

def get_preprocessor():
    # Define columns
    numeric_features = ['IAA', 'IEG', 'IPS', 'IDA', 'Matem', 'Portug', 'Inglês', 'IPV', 'IAN', 'Média_Geral']
    categorical_features = ['Fase', 'Pedra'] # Assuming 'Pedra' or 'Fase ideal' exists, need to verify strict columns from EDA. 
    # Based on EDA: 'Fase ideal' exists. 'Pedra' I haven't seen but usually exists.
    # I saw 'Fase ideal', 'Destaque IEG', 'Destaque IDA', 'Destaque IPV' in the head output.
    
    categorical_features = ['Fase ideal', 'Destaque IEG', 'Destaque IDA', 'Destaque IPV']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Columns to drop (IDs or Leakage)
    drop_cols = ['Nome', 'Avaliador1', 'Rec Av1', 'Avaliador2', 'Rec Av2', 'Avaliador3', 'Rec Av3', 
                 'Avaliador4', 'Rec Av4', 'Rec Psicologia', 'Indicado', 'Atingiu PV', 'Alune', 'PEDE 2022', 'PEDE 2023'] # Generic list

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop' # Drop other columns not specified? Or passthrough? 
        # Safer to be explicit or use 'drop' for unknown cols.
        # But I need to handle 'Defas' separately (it's y).
    )
    
    return preprocessor
