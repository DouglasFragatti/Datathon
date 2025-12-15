import pytest
from src.preprocessing import get_preprocessor
import pandas as pd

def test_preprocessor_structure():
    prep = get_preprocessor()
    # It returns a ColumnTransformer
    assert prep is not None
    # We can't easily fit_transform here without matching columns exactly,
    # but we can check the object type.
    from sklearn.compose import ColumnTransformer
    assert isinstance(prep, ColumnTransformer)
