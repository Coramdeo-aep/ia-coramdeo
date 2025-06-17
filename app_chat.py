
import streamlit as st
from groq import Groq

# CONFIGURAÇÃO
st.set_page_config(page_title="IA Corporativa", layout="wide")

# INICIALIZAÇÃO DO CLIENTE GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# HISTÓRICO DA CONVERSA
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# TÍTULO
st.title("🤖 IA Corporativa - Consulta de Arquivos")

# ENTRADA DO USUÁRIO
user_input = st.text_input("Digite sua pergunta sobre os documentos:", key="user_input")

# PROCESSAMENTO DA RESPOSTA
if user_input:
    with st.spinner("Consultando IA..."):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Você é um assistente que responde com base em documentos técnicos corporativos armazenados no Google Drive."},
                    {"role": "user", "content": user_input}
                ],
                model="llama3-8b-8192"
            )
            answer = response.choices[0].message.content
            st.session_state.chat_history.append(("Você", user_input))
            st.session_state.chat_history.append(("IA", answer))
        except Exception as e:
            st.error(f"Erro ao consultar a IA: {e}")

# EXIBIR CONVERSA
st.markdown("### Histórico")
for autor, msg in st.session_state.chat_history[::-1]:
    st.markdown(f"**{autor}:** {msg}")
