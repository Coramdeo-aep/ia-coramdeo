import streamlit as st
import requests
import json

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
        # Envia a requisição, ignorando SSL (para ambiente de testes)
        response = requests.post(url, json=payload, verify=False)
        print("Status code:", response.status_code)
        print("Resposta bruta:", repr(response.text))

        if response.status_code == 200 and response.text.strip():
            text = response.content.decode('utf-8')
            data = json.loads(text)

            if isinstance(data, list) and data and isinstance(data[0], dict):
                resposta = data[0].get("resposta", "⚠️ Resposta não encontrada.")
            elif isinstance(data, dict):
                resposta = data.get("resposta", "⚠️ Resposta não encontrada.")
            else:
                resposta = "⚠️ Formato de resposta inesperado."
        else:
            resposta = f"⚠️ Erro na resposta: status {response.status_code} | corpo vazio"

    except Exception as e:
        resposta = f"Erro ao conectar: {e}"

    # Atualiza o histórico de mensagens
    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta))

# Exibe o histórico de conversas (última mensagem primeiro)
for speaker, msg in st.session_state.history[::-1]:
    if speaker == "IA":
        # Aplica formatação HTML leve com quebra de linha
        styled_msg = msg.replace("\n", "<br>")

        st.markdown(f"""
            <div style="background-color: #f5f5f5; border-left: 4px solid #4CAF50; padding: 10px; border-radius: 6px; margin-top: 10px;">
                <strong>{speaker}:</strong><br>{styled_msg}
            </div>
        """, unsafe_allow_html=True)
    else:
        # Estilo para mensagem do usuário
        st.markdown(f"""
            <div style="background-color: #e8f0fe; padding: 10px; border-radius: 6px; margin-top: 10px;">
                <strong>{speaker}:</strong><br>{msg}
            </div>
        """, unsafe_allow_html=True)
