import os
from dotenv import load_dotenv
import requests
import pandas as pd
from groq import Groq

# ------------------- Configuração para API key --------------------
# carrega as variáveis do arquivo .env para o sistema
load_dotenv()
# busca a chave das variáveis de ambiente do sistema
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# -------------------------- E -> EXTRACT ---------------------------
def get_user(id):
    # um serviço que tem dados falsos de uma empresa 
    url = f'https://jsonplaceholder.typicode.com/users/{id}'
    # requisição no URL
    response = requests.get(url)
    # se status = 200 (SUCESSO) -> transforma o JSON em dicionario
    # se não, retorna None 
    return response.json() if response.status_code == 200 else None

# -------------------------- T -> TRANSFORM --------------------------
def process_user_data(users):
    return {
        "id": users['id'],
        "nome_completo": users['name'],
        "empresa": users['company']['name'],
        "cidade": users['address']['city'],
        "email_corporativo": users['email'].lower()
    }

# -------------------------- Consome API de Groq --------------------------
def generate_ai_message(user):
    prompt = f"Escreva uma mensagem de boas-vindas personalizada para {user['name']}, que trabalha na empresa {user['company']['name']} sobre importância dos investimentos (máximo 100 caracteres)."
    try:
        completion = client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {"role": "system", "content": "Você é especialista em marketing bancário."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Alerta: Falha ao gerar mensagem para {user['name']}: {e}")
        return f"Olá, descubra o poder dos investimentos para o seu futuro!"

# -------------------------- L -> LOAD --------------------------
def update_user(user):
    # endpoint para atualizar um recurso existente é o PUT
    url = f"https://jsonplaceholder.typicode.com/users/{user['id']}"
    # enviar o objeto do usuário que tem mensagem do IA agora
    response = requests.put(url, json=user)

    if response.status_code == 200:
        print(f"✅ Usuário {user['nome_completo']} atualizado com sucesso na API!\n")
        # print(f"📡 Resposta da API: {response.json()}")
        return True
    else:
        print(f"❌ Erro ao atualizar usuário {user['id']}: {response.status_code}\n")
        return False


# ----------------------- EXECUÇÃO DO PIPELINE -----------------------
user_ids = [1, 2, 3, 4, 5]
final_users = []

# busca todos dados de usuários com ID da lista
for id in user_ids:
    # EXTRACT
    user = get_user(id)
    # garante que tem usuario
    if user:
        # chama a IA para cada usuário
        print(f"Processando mensagem para: {user['name']}...")
        message_ai = generate_ai_message(user)
        print(message_ai)

        # TRANSFORM: processa os dados (limpeza)
        user_process = process_user_data(user)
        # adciona mensagem da IA ao dicionario processado
        user_process['message'] = message_ai
        
        success = update_user(user_process)
        if success: 
            # guarda resultado completo na lista final
            final_users.append(user_process)


# configuração para visualização no terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 30)
pd.set_option('display.width', 1000)

# converter em tabela (data frame)
df = pd.DataFrame(final_users)
print("\n--- RESULTADO FINAL DO PIPELINE ---")
print(df)
# salva em .csv o versão final
df.to_csv('relatorio_final.csv', index=False)
print("\nPipeline concluído! Arquivo 'relatorio_final.csv' gerado.")
