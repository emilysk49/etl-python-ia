import pandas as pd
import requests

# Extract - consumindo API pronto de animes
url = "https://api.jikan.moe/v4/top/anime"

# Faz requisição do url
response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    lista_animes = dados['data']
    # Transform - usando panda
    df = pd.DataFrame(lista_animes)

    # filtrando animes com score acima de 8.5
    df_filtrado = df[['title', 'score', 'episodes']].query("score > 8.5")

    print("Animes com score maior que 8.5 :")
    print(df_filtrado)
    
    # Load (Salvando o resultado)
    df_filtrado.to_csv('top_animes.csv', index=False)
else:
    print(f"Erro ao acessar a API: {response.status_code}")