import streamlit as st
import requests
from groq import Groq

# ---- CONFIGURAÇÕES ----
st.set_page_config(page_title="IA Coram Deo", page_icon="🤖", layout="wide")

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_ANON_KEY = st.secrets["supabase"]["key"]
GROQ_API_KEY = st.secrets["groq"]["api_key"]
TABELA = "documentos"

client = Groq(api_key=GROQ_API_KEY)

# ---- FUNÇÃO PRINCIPAL ----
def responder_pergunta(pergunta):
    st.info("🔍 Buscando documentos no Supabase...")

    url = f"{SUPABASE_URL}/rest/v1/{TABELA}?select=conteudo"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except Exception as e:
        st.error(f"Erro ao buscar documentos: {e}")
        return

    docs = [item['conteudo'] for item in r.json() if 'conteudo' in item]

    # Estimar quantidade de tokens (1 token ≈ 4 caracteres)
    max_tokens_total = 6000
    max_tokens_resposta = 500
    max_tokens_contexto = max_tokens_total - max_tokens_resposta
    max_chars = max_tokens_contexto * 4  # ≈ 22.000 caracteres

    contexto = ""
    total_chars = 0

    for doc in docs:
        if total_chars + len(doc) <= max_chars:
            contexto += "\n\n" + doc
            total_chars += len(doc)
        else:
            break

    prompt = f"""
Você é um assistente da Associação Coram Deo.
Responda com base apenas no conteúdo a seguir:

{contexto}

Pergunta: {pergunta}
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=max_tokens_resposta
        )
        resposta = response.choices[0].message.content
        st.success("✅ Resposta da IA:")
        st.markdown(resposta)
    except Exception as e:
        st.error("❌ Erro ao obter resposta da IA:")
        st.exception(e)

# ---- INTERFACE ----
st.title("🤖 IA Coram Deo")
st.write("Faça uma pergunta e receba uma resposta baseada nos documentos da base de dados.")

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    responder_pergunta(pergunta)
