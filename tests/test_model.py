import pytest
import pandas as pd
from src.preprocessing import get_preprocessor
from src.feature_engineering import FeatureEngineer

def test_feature_engineer():
    fe = FeatureEngineer()
    df = pd.DataFrame({'Portug': [5], 'Matem': [7], 'Inglês': [9]})
    res = fe.transform(df)
    assert 'Média_Geral' in res.columns
    assert res['Média_Geral'][0] == 7.0

def test_pipeline_integration():
    # Only verify we can instantiate it
    prep = get_preprocessor()
    assert prep is not None
