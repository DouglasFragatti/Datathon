import pandas as pd
import os

file_path = r"c:\Projetos\Tech5\data\BASE DE DADOS PEDE 2024 - DATATHON.xlsx"

try:
    print(f"Loading {file_path}...")
    df = pd.read_excel(file_path)
    print("Dataset Loaded Successfully!")
    print("\n--- Shape ---")
    print(df.shape)
    print("\n--- Columns ---")
    print(df.columns.tolist())
    print("\n--- Head ---")
    print(df.head(2).to_string())
    print("\n--- Missing Values ---")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print("\n--- Types ---")
    print(df.dtypes)
except Exception as e:
    print(f"Error loading data: {e}")
