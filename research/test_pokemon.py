import pandas as pd
import kagglehub 
from kagglehub import KaggleDatasetAdapter
import matplotlib.pyplot as plt
"""
Pandas permite trabalhar com: dados tabulares (excel, sql), dados ordenados, ...
- Serie: matriz unidimencional (parecida com uma unica coluna no Excel) -> tipo lista
- DataFrame: estrutura de dados tabular, semelhante a planilha do Excel


df.shape -> retorna (total_linhas, total_colunas)
df.info -> informa tipos de dados 
df.isnull -> quantos dados faltantes em cada coluna
df['coluna1'].unique() -> retorna valores unicos da coluna1
df['coluna1'].value_counts().plot(kind='bar) -> cria grafico
"""

# arquivo do pokemon dentro do Rounak Banik
file_path = "pokemon.csv"

# criar df
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "rounakbanik/pokemon",
    file_path
)

# legendarys = df.query("is_legendary == 1")
# print("Pokemons lendários e geração dele:")
# print(legendarys[['name', 'generation']])

# lendarios 
df_lendarios = df[df['is_legendary'] == 1]

# tipos = df['type1'].unique()
contagem_t1 = df_lendarios['type1'].value_counts()
contagem_t2 = df_lendarios['type2'].value_counts()

# fill_value=0 garante que tipos que só existem no T1 não virem NaN
total_tipos = contagem_t1.add(contagem_t2, fill_value=0).sort_values(ascending=False)
total_tipos.plot(kind='bar')
plt.title("Quantidade por Tipagem - Pokemon Lendário")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()