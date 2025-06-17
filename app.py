import streamlit as st
from supabase_utils import buscar_contexto_documentos
from llm_utils import perguntar_para_ia

st.set_page_config(page_title="Chat Coram Deo", page_icon="📚")
st.title("🤖 Chat Institucional - Coram Deo")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    with st.spinner("Consultando documentos..."):
        contexto = buscar_contexto_documentos()
        resposta = perguntar_para_ia(pergunta, contexto)
        st.session_state.mensagens.append(("Você", pergunta))
        st.session_state.mensagens.append(("IA Coram Deo", resposta))

for remetente, msg in st.session_state.mensagens:
    st.chat_message(remetente).markdown(msg)
