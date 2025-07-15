import streamlit as st
import requests

# URL do webhook do n8n
N8N_WEBHOOK_URL = "https://n8n.diferro.com.br:5678/webhook/chat"

st.title("Chat com n8n")

# Caixa de entrada do usuário
mensagem = st.text_input("Digite sua mensagem:")

# Botão para enviar
if st.button("Enviar"):
    if mensagem.strip() == "":
        st.warning("Digite algo antes de enviar.")
    else:
        # Enviando a mensagem para o n8n
        payload = [{"mensagem": mensagem}]
        try:
            resposta = requests.post(N8N_WEBHOOK_URL, json=payload, verify=False)
            if resposta.status_code == 200:
                dados = resposta.json()
                st.success("Resposta do n8n:")
                st.markdown(dados[0]["output"])
            else:
                st.error(f"Erro ao contatar o n8n: {resposta.status_code}")
        except Exception as e:
            st.error(f"Erro na requisição: {e}")
