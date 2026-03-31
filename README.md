# 🚀 Python ETL Pipeline: API Integration & AI Enrichment
Este projeto é um pipeline de **Extract, Transform, Load (ETL)** que consome dados de uma API, utiliza Inteligência Artificial (**Llama 3.1 via Groq**) para gerar insights personalizados e atualiza os registros de volta na nuvem.

## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** Python 3.13
* **Manipulação de Dados:** Pandas
* **Integração de IA:** Groq Cloud API (Modelo `llama-3.1-8b-instant`)
* **Consumo de APIs:** Requests
* **Segurança:** Python-dotenv (Gestão de variáveis de ambiente)

## 📂 Estrutura de Arquivos
O repositório está dividido para mostrar a evolução do desenvolvimento:

* **`/src`**: Código de produção com o pipeline finalizado, tratamento de erros e logs.
* **`/research`**: Laboratórios de estudo onde explorei manipulação de DataFrames com datasets de **Pokémon** e consumo de APIs de **Anime**.

## 🔄 Fluxo de Processamento (ETL)

1.  **Extract**: Consumo de dados de usuários via JSONPlaceholder API.
2.  **Transform**: 
    * Limpeza e normalização de strings.
    * Geração de mensagens personalizadas sobre investimentos usando IA (Groq).
    * Implementação de **Fallbacks** (se a IA falhar, o sistema providencia uma mensagem padrão).
3.  **Load**: 
    * Simulação de `PUT` para atualizar os dados na API original.
    * Geração de arquivo CSV (`auditoria_usuarios.csv`) para conferência visual.
  
## 🚀 Como Executar
1. Clone o repositório: `git clone https://github.com/emilysk49/etl-python-ia.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` baseado no `.env.example` e insira sua `GROQ_API_KEY`.
4. Execute: `python src/etl_final.py`
