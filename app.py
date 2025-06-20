# streamlit_app.py

import streamlit as st
import requests

# Configuração
WEBHOOK_URL = "https://n8n.diferro.com.br:5678/webhook/chat-coramdeo"

st.title("🤖 Chat com a IA (via n8n Webhook)")

# Entrada do usuário
user_input = st.text_input("Digite sua pergunta:", "")

# Quando enviar
if st.button("Enviar") and user_input:
    # Envia para o webhook do n8n
    response = requests.post(WEBHOOK_URL, json={"pergunta": user_input})

    # Exibe resposta
    if response.status_code == 200:
        resposta = response.json().get("resposta", "Sem resposta definida.")
        st.markdown(f"**Resposta da IA:** {resposta}")
    else:
        st.error(f"Erro ao conectar com a IA: {response.status_code}")
