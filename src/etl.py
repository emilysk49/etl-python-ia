import os
from dotenv import load_dotenv
import requests
import pandas as pd
from groq import Groq

# carrega as variáveis do arquivo .env para o sistema
load_dotenv()

# busca a chave das variáveis de ambiente do sistema
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def get_user(id):
    # um serviço que tem dados falsos de uma empresa 
    url = f'https://jsonplaceholder.typicode.com/users/{id}'
    # requisição no URL
    response = requests.get(url)
    # se status = 200 (SUCESSO) -> transforma o JSON em dicionario
    # se não, retorna None 
    return response.json() if response.status_code == 200 else None

def process_user_data(users):
    return {
        "id": users['id'],
        "nome_completo": users['name'],
        "empresa": users['company']['name'],
        "cidade": users['address']['city'],
        "email_corporativo": users['email'].lower()
    }

def generate_ai_message(user):
    prompt = f"Escreva uma mensagem de boas-vindas personalizada para {user['name']}, que trabalha na empresa {user['company']['name']} sobre importância dos investimentos (máximo 100 caracteres)."
    completion = client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=[
            {"role": "system", "content": "Você é especialista em marketing bancário."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


user_ids = [1, 2, 3, 4, 5]
final_users = []
# busca todos dados de usuários com ID da lista
for id in user_ids:
    user = get_user(id)
    # garante que tem usuario
    if user:
        print(f"Processando mensagem para: {user['name']}...")
        # chama a IA para cada usuário
        message_ai = generate_ai_message(user)
        print(message_ai)
        print()

        # processa os dados (limpeza)
        user_process = process_user_data(user)

        # adciona mensagem da IA ao dicionario processado
        user_process['message'] = message_ai
        
        # guarda resultado completo na lista final
        final_users.append(user_process)

# converter em tabela (data frame)
df = pd.DataFrame(final_users)
print(df)
# salva em .csv o versão final
df.to_csv('auditoria_usuarios.csv', index=False)

