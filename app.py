import streamlit as st
import requests

# URL do seu webhook do n8n
N8N_WEBHOOK_URL = "https://n8n.diferro.com.br:5678/webhook-test/chat"

st.title("Assistente Diferro com n8n")
st.write("Você está conversando com um assistente conectado ao n8n. Envie sua pergunta abaixo:")

# Inicializa histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico no chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto (chat_input)
if prompt := st.chat_input("Digite sua pergunta:"):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envia a mensagem para o n8n
    try:
        payload = {"mensagem": prompt}
        resposta = requests.post(N8N_WEBHOOK_URL, json=payload, verify=False)
        
        if resposta.status_code == 200:
            dados = resposta.json()

            # Extrai resposta do campo "output"
            output = dados[0].get("output", "Erro: Campo 'output' não encontrado.")

            # Exibe e armazena a resposta do n8n
            with st.chat_message("assistant"):
                st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        else:
            erro_msg = f"Erro ao contatar o n8n: Status {resposta.status_code}"
            with st.chat_message("assistant"):
                st.error(erro_msg)
            st.session_state.messages.append({"role": "assistant", "content": erro_msg})
    
    except Exception as e:
        erro_msg = f"Erro na requisição: {e}"
        with st.chat_message("assistant"):
            st.error(erro_msg)
        st.session_state.messages.append({"role": "assistant", "content": erro_msg})
