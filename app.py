import streamlit as st
import requests
import certifi

st.set_page_config(page_title="Chat com IA - Diferro", layout="centered")

st.title("🤖 Chat IA Diferro")

# Histórico
if "history" not in st.session_state:
    st.session_state.history = []

# Input do usuário
user_input = st.text_input("Digite sua pergunta:", key="input")

if st.button("Enviar") and user_input:
    url = "https://n8n.diferro.com.br:5678/webhook/chat"
    payload = {"chatInput": user_input}

    try:
        # Passa o caminho dos certificados para o requests validar SSL corretamente
        response = requests.post(url, json=payload, verify=certifi.where())
        resposta = response.json().get("resposta", "⚠️ Resposta não encontrada.")
    except Exception as e:
        resposta = f"Erro ao conectar: {e}"

    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta))

for speaker, msg in st.session_state.history[::-1]:
    st.markdown(f"**{speaker}:** {msg}")
