import streamlit as st
import requests
import urllib3

# Desativa warnings de SSL inseguros (para teste)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WEBHOOK_URL = "https://n8n.diferro.com.br:5678/webhook-test/chat-coramdeo"

st.title("🤖 Chat com a IA (via n8n Webhook)")

user_input = st.text_input("Digite sua pergunta:", "")

if st.button("Enviar") and user_input:
    try:
        # Envia POST ignorando verificação SSL
        response = requests.post(WEBHOOK_URL, json={"pergunta": user_input}, verify=False)

        if response.status_code == 200:
            resposta = response.json().get("resposta", "Sem resposta definida.")
            st.markdown(f"**Resposta da IA:** {resposta}")
        else:
            st.error(f"Erro ao conectar com a IA: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
