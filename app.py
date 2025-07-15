import streamlit as st
import requests
import json
import re

# Configuração da página
st.set_page_config(page_title="Chat IA Diferro", layout="centered", initial_sidebar_state="collapsed")

# Paleta de cores
PRIMARY_COLOR = "#D10007"
USER_COLOR = "#000000"
BG_COLOR = "#ffffff"

# Histórico de conversa
if "history" not in st.session_state:
    st.session_state.history = []

# Mensagem para resposta (modo reply)
if "reply_to" not in st.session_state:
    st.session_state.reply_to = None

# Estilo CSS
st.markdown(f"""
<style>
    body {{ background-color: {BG_COLOR}; }}
    .chat-container {{
        margin-top: 20px;
    }}
    .bubble {{
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 16px;
        transition: all 0.3s ease;
    }}
    .user {{
        background-color: #eeeeee;
        color: {USER_COLOR};
        align-self: flex-end;
    }}
    .ia {{
        background-color: #f9e6e6;
        border-left: 4px solid {PRIMARY_COLOR};
        color: #333;
        align-self: flex-start;
    }}
    .reply {{
        font-size: 13px;
        color: #888;
        margin-bottom: 5px;
    }}
    .icon-button {{
        background: none;
        border: none;
        color: {PRIMARY_COLOR};
        cursor: pointer;
        font-size: 18px;
        margin-left: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown(f"<h1 style='color:{PRIMARY_COLOR}'>🤖 Chat IA Diferro</h1>", unsafe_allow_html=True)

# Botões de ação
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧹 Limpar histórico"):
        st.session_state.history = []

# Input de texto com Enter
user_input = st.text_input("Digite sua pergunta e pressione Enter", key="input", label_visibility="collapsed")

if user_input:
    # Envia mensagem
    url = "https://n8n.diferro.com.br:5678/webhook/chat"
    payload = {"chatInput": user_input}

    try:
        response = requests.post(url, json=payload, verify=False)
        dados = json.loads(response.text)
        resposta = dados.get("output", "⚠️ Resposta não encontrada.")
        resposta_formatada = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", resposta)
    except Exception as e:
        resposta_formatada = f"Erro ao conectar: {e}"

    if st.session_state.reply_to:
        user_input = f"(Em resposta a: {st.session_state.reply_to})\n{user_input}"
        st.session_state.reply_to = None

    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("IA", resposta_formatada))
    st.experimental_rerun()  # Atualiza automaticamente

# Área de exibição de mensagens
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i in range(len(st.session_state.history)-1, -1, -1):
    speaker, msg = st.session_state.history[i]

    # Estilo da mensagem
    role_class = "user" if speaker == "Você" else "ia"
    icon = "↩️" if speaker == "IA" else "👤"

    reply_btn = ""
    if speaker == "IA":
        reply_btn = f"""
        <form action="" method="post">
            <button class="icon-button" name="reply_{i}">↩️</button>
        </form>
        """

    if f"reply_{i}" in st.experimental_get_query_params():
        st.session_state.reply_to = msg
        st.experimental_rerun()

    # Renderiza mensagem
    styled_msg = msg.replace("\n", "<br>")
    st.markdown(f"""
        <div class="bubble {role_class}">
            <div class="reply">{icon} <strong>{speaker}</strong> {reply_btn}</div>
            <div>{styled_msg}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
