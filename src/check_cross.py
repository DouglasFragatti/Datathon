import pandas as pd
try:
    df = pd.read_excel(r'c:\Projetos\Tech5\data\BASE DE DADOS PEDE 2024 - DATATHON.xlsx')
    print("--- Indicado vs Defas ---")
    print(pd.crosstab(df['Indicado'], df['Defas']))
    print("\n--- Mean INDE by Indicado ---")
    print(df.groupby('Indicado')['INDE 22'].mean())
except Exception as e:
    print(e)
