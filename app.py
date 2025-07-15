import streamlit as st
import requests
import json

st.set_page_config(page_title="Chat com IA - Diferro", layout="centered")
st.title("🤖 Chat IA Diferro")

# Histórico
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Digite sua pergunta:", key="input")

if st.button("Enviar") and user_input:
    url = "https://n8n.diferro.com.br:5678/webhook/chat"
    payload = {"chatInput": user_input}

    try:
        response = requests.post(url, json=payload, verify=False)

        dados = json.loads(response.text)
        resposta = dados[0].get("output", "⚠️ Resposta não encontrada.")  # <- pega da lista

    except Exception as e:
        resposta = f"Erro ao conectar: {e}"

    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta))

# Exibe mensagens
for speaker, msg in st.session_state.history[::-1]:
    st.markdown(f"**{speaker}:**")
    st.markdown(msg)
