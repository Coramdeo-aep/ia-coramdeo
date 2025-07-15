import streamlit as st
import requests

st.set_page_config(page_title="Chat com IA - Diferro", layout="centered")
st.title("🤖 Chat IA Diferro")

# Histórico
if "history" not in st.session_state:
    st.session_state.history = []

# Input
user_input = st.text_input("Digite sua pergunta:", key="input")

if st.button("Enviar") and user_input:
    url = "https://n8n.diferro.com.br:5678/webhook/chat"
    payload = {"chatInput": user_input}

    try:
        response = requests.post(url, json=payload, verify=False)

        # Usando response.json() — equivalente a json.load
        dados = response.json()
        resposta = dados.get("resposta", "⚠️ Resposta não encontrada.")

    except Exception as e:
        resposta = f"Erro ao conectar: {e}"

    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta))

# Exibição
for speaker, msg in st.session_state.history[::-1]:
    if speaker == "IA":
        styled_msg = msg.replace("\n", "<br>")
        st.markdown(f"""
            <div style="background-color: #f5f5f5; border-left: 4px solid #4CAF50; padding: 10px; border-radius: 6px; margin-top: 10px;">
                <strong>{speaker}:</strong><br>{styled_msg}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background-color: #e8f0fe; padding: 10px; border-radius: 6px; margin-top: 10px;">
                <strong>{speaker}:</strong><br>{msg}
            </div>
        """, unsafe_allow_html=True)
