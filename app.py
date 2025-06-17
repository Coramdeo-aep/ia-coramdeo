import streamlit as st
import requests
import os
from groq import Groq

# Configurações (configure as variáveis de ambiente no Streamlit Cloud)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
TABELA = os.getenv("TABELA")

# Groq API - Ajuste conforme seu SDK ou uso da API REST
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your-groq-api-key"
GROQ_API_URL = "https://api.groq.ai/v1/chat/completions"  

headers_supabase = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Accept": "application/json",
}

st.set_page_config(page_title="Coram Deo IA Consultiva", layout="wide")

st.markdown("""
# 🧠 Coram Deo - Assistente Inteligente  
*Pergunte algo e receba respostas baseadas nos documentos institucionais.*
""")

if "historico" not in st.session_state:
    st.session_state.historico = []

def buscar_contexto():
    try:
        url = f"{SUPABASE_URL}/rest/v1/{TABELA}?select=conteudo"
        r = requests.get(url, headers=headers_supabase)
        r.raise_for_status()
        docs = [item['conteudo'] for item in r.json()]

        max_chars = 15000
        contexto = ""
        for doc in docs:
            if len(contexto) + len(doc) <= max_chars:
                contexto += "\n\n" + doc
            else:
                break
        return contexto
    except Exception as e:
        st.error(f"Erro ao buscar documentos: {e}")
        return ""

def enviar_pergunta_groq(pergunta, contexto):
    prompt = f"""
Responda com base apenas no conteúdo a seguir:

{contexto}

Pergunta: {pergunta}
"""
    try:
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1024,
        }
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        resposta = data["choices"][0]["message"]["content"]
        return resposta
    except Exception as e:
        return f"Erro na API Groq: {e}"

with st.form("form_pergunta", clear_on_submit=True):
    pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Qual a missão da Coram Deo?")
    enviar = st.form_submit_button("Perguntar")

if enviar and pergunta:
    with st.spinner("Consultando documentos e gerando resposta..."):
        contexto = buscar_contexto()
        if contexto:
            resposta = enviar_pergunta_groq(pergunta, contexto)
        else:
            resposta = "Não foi possível obter o contexto dos documentos."

        # Atualiza histórico
        st.session_state.historico.append({"pergunta": pergunta, "resposta": resposta})

# Exibir histórico com estilo GPT-like
for item in reversed(st.session_state.historico):
    st.markdown(f"**Você:** {item['pergunta']}")
    st.markdown(f"**IA Coram Deo:** {item['resposta']}")
    st.markdown("---")

# CSS para deixar visual mais corporativo
st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #555;
    }
    .stButton>button {
        background-color: #FF6F00;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
    }
    .stMarkdown p {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
