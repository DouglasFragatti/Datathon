import pandas as pd
try:
    df = pd.read_excel(r'c:\Projetos\Tech5\data\BASE DE DADOS PEDE 2024 - DATATHON.xlsx')
    print("--- Indicado ---")
    print(df['Indicado'].value_counts(dropna=False))
    print("\n--- Atingiu PV ---")
    print(df['Atingiu PV'].value_counts(dropna=False))
except Exception as e:
    print(e)
