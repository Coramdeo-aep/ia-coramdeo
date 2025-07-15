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

        # Interpreta a resposta como JSON
        dados = json.loads(response.text)
        resposta = dados.get("output", "⚠️ Resposta não encontrada.")

    except Exception as e:
        resposta = f"Erro ao conectar: {e}"

    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta))

# Exibe as mensagens com Markdown nativo
for speaker, msg in st.session_state.history[::-1]:
    if speaker == "IA":
        st.markdown(f"**{speaker}:**")
        st.markdown(msg)  # renderiza Markdown nativamente
    else:
        st.markdown(f"**{speaker}:** {msg}")
