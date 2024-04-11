import pandas as pd

# Cria um DataFrame de exemplo
dados = {'A': [1, 2, 3, 4, 5],
         'B': ['a', 'b', 'c', 'd', 'e']}
df = pd.DataFrame(dados)

# Verifica se o elemento 'c' está na coluna 'B' usando isin()
if df['B'].isin(['c']).any() == False:
    print("O elemento 'c' está na coluna 'B'")
else:
    print("O elemento 'c' não está na coluna 'B'")

print(df['B'].isin(['c']).any())