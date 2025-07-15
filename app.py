import streamlit as st
import requests

st.set_page_config(page_title="Chat com IA - Diferro", layout="centered")

st.title("🤖 Chat IA Diferro")

# Histórico
if "history" not in st.session_state:
    st.session_state.history = []

# Input do usuário
user_input = st.text_input("Digite sua pergunta:", key="input")

if st.button("Enviar") and user_input:
    url = "https://n8n.diferro.com.br:5678/webhook-test/chat"  # coloque o endereço real do webhook aqui
    payload = {"chatInput": user_input}

    try:
        # Pula a verificação de SSL para testes
        response = requests.post(url, json=payload, verify=False)
        resposta = response.json().get("resposta", "⚠️ Resposta não encontrada.")
    except Exception as e:
        resposta = f"Erro ao conectar: {e}"

    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta))

for speaker, msg in st.session_state.history[::-1]:
    st.markdown(f"**{speaker}:** {msg}")
