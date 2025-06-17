import streamlit as st
import os
from google.oauth2 import service_account
from drive_utils import exportar_drive_para_local, autenticar_drive
from extract_utils import extrair_pdf, extrair_docx, extrair_html, extrair_planilha
from supabase_utils import documento_existe, inserir_documento, buscar_conteudos
from groq_utils import responder_pergunta
from config import FOLDER_ID, PASTA_BASE


st.set_page_config(page_title="IA + Drive + Supabase", layout="wide")

st.title("📚 IA + Google Drive + Supabase + Groq (Llama3)")

with st.sidebar:
    st.header("🔗 Google Drive")
    google_json = st.file_uploader("Suba seu arquivo de chave JSON do Google (Service Account)", type=['json'])

    if google_json:
        creds = service_account.Credentials.from_service_account_info(
            eval(google_json.getvalue().decode())
        )
        drive_service = autenticar_drive(creds)

        if st.button("📥 Baixar arquivos do Drive"):
            exportar_drive_para_local(FOLDER_ID, PASTA_BASE, drive_service)
            st.success("Arquivos baixados!")

st.subheader("🔍 Indexar Arquivos")

if st.button("🔗 Indexar para Supabase"):
    tipos_validos = ['.pdf', '.docx', '.html', '.xlsx', '.xls', '.csv']
    novos = 0

    for root, dirs, files in os.walk(PASTA_BASE):
        for file in files:
            if not any(file.endswith(ext) for ext in tipos_validos):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, PASTA_BASE)

            if documento_existe(rel_path):
                continue

            ext = os.path.splitext(file)[1]
            if ext == ".pdf":
                texto = extrair_pdf(full_path)
            elif ext == ".docx":
                texto = extrair_docx(full_path)
            elif ext == ".html":
                texto = extrair_html(full_path)
            elif ext in [".csv", ".xls", ".xlsx"]:
                texto = extrair_planilha(full_path)
            else:
                texto = ""

            if texto.strip():
                if inserir_documento(file, rel_path, ext, texto):
                    novos += 1

    st.success(f"✅ Indexação finalizada. Novos arquivos adicionados: {novos}")

st.subheader("🤖 Pergunte para a IA sobre seus documentos")

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    documentos = buscar_conteudos()
    contexto = "\n\n".join(documentos)[:15000]
    resposta = responder_pergunta(pergunta, contexto)
    st.markdown(f"**🧠 Resposta:** {resposta}")
