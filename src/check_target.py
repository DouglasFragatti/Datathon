import pandas as pd
try:
    df = pd.read_excel(r'c:\Projetos\Tech5\data\BASE DE DADOS PEDE 2024 - DATATHON.xlsx')
    print("--- Target Distribution (Defas) ---")
    print(df['Defas'].value_counts(dropna=False))
    print("\n--- Correlation with Target ---")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    print(numeric_df.corr()['Defas'].sort_values(ascending=False))
except Exception as e:
    print(e)
