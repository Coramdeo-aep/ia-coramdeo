import streamlit as st
from supabase_utils import buscar_contexto
from llm_utils import perguntar_para_ia

st.set_page_config(page_title="Chat Coram Deo", page_icon="🧠")

st.title("🤖 Chat da Coram Deo")
st.markdown("Converse com a IA treinada com os dados institucionais.")

# Estado da conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Campo de entrada
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    with st.spinner("Consultando base de dados..."):
        contexto = buscar_contexto()
        resposta = perguntar_para_ia(pergunta, contexto)
        st.session_state.mensagens.append(("Você", pergunta))
        st.session_state.mensagens.append(("IA Coram Deo", resposta))

# Mostrar conversa
for remetente, msg in st.session_state.mensagens:
    st.chat_message(remetente).markdown(msg)
