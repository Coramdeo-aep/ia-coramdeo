import streamlit as st
import requests
import pdfplumber
from PIL import Image
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import docx
from bs4 import BeautifulSoup

# ----------- CONFIG -----------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# ----------- AUTENTICAR GOOGLE -----------
@st.cache_resource(show_spinner=False)
def autenticar_drive():
    auth.authenticate_user()
    return build('drive', 'v3')

drive_service = autenticar_drive()

# ----------- LISTAR ARQUIVOS -----------
def listar_arquivos_recursivo(service, folder_id):
    arquivos = []
    resultados = service.files().list(q=f"'{folder_id}' in parents and trashed = false",
                                      fields="files(id, name, mimeType)").execute().get('files', [])
    for arq in resultados:
        arquivos.append(arq)
        if arq['mimeType'] == 'application/vnd.google-apps.folder':
            arquivos.extend(listar_arquivos_recursivo(service, arq['id']))
    return arquivos

# ----------- DOWNLOAD E EXTRAÇÃO -----------
def baixar_arquivo(file_id, nome):
    caminho = os.path.join("arquivos", nome)
    os.makedirs("arquivos", exist_ok=True)
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(caminho, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return caminho

def extrair_texto(arquivo):
    texto = ""
    if arquivo.endswith(".pdf"):
        with pdfplumber.open(arquivo) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() or ""
    elif arquivo.endswith(".docx"):
        doc = docx.Document(arquivo)
        texto = "\n".join([p.text for p in doc.paragraphs])
    elif arquivo.endswith(".html"):
        with open(arquivo, encoding="utf-8") as f:
            texto = BeautifulSoup(f, "html.parser").get_text()
    elif arquivo.endswith(".png") or arquivo.endswith(".jpg"):
        # Imagens ignoradas para OCR local - opcional: indicar que não extraiu texto
        texto = "[Imagem - extração de texto via OCR não suportada no ambiente atual]"
    elif arquivo.endswith(".txt"):
        with open(arquivo, encoding="utf-8") as f:
            texto = f.read()
    return texto

# ----------- PERGUNTA À IA -----------
def perguntar_groq(pergunta, contexto):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Você é um assistente que responde com base nos documentos institucionais da Coram Deo."},
            {"role": "user", "content": f"Contexto:\n{contexto[:12000]}"},
            {"role": "user", "content": pergunta}
        ],
        "temperature": 0.2
    }
    r = requests.post(GROQ_ENDPOINT, json=data, headers=headers)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    return f"Erro: {r.status_code}\n{r.text}"

# ----------- INTERFACE STREAMLIT -----------
st.set_page_config(page_title="Assistente Coram Deo", layout="wide")
st.title("🤖 Assistente Coram Deo")

folder_id = st.text_input("ID da pasta principal do Google Drive:", value="1dyyR6Hz3_VkROH9XwB4YF6KukxEDwpdY")

if st.button("🔍 Carregar e processar documentos"):
    arquivos = listar_arquivos_recursivo(drive_service, folder_id)
    contexto_total = ""
    with st.spinner("Lendo arquivos..."):
        for arq in arquivos:
            if arq['mimeType'] == 'application/pdf' or arq['name'].endswith((".pdf", ".docx", ".txt", ".html", ".png", ".jpg")):
                nome_local = baixar_arquivo(arq['id'], arq['name'])
                texto = extrair_texto(nome_local)
                contexto_total += f"\n=== {arq['name']} ===\n{texto}\n"
    st.session_state['contexto'] = contexto_total
    st.success("Documentos processados com sucesso!")

if 'contexto' in st.session_state:
    pergunta = st.text_area("Digite sua pergunta sobre a Coram Deo:")
    if st.button("Perguntar"):
        resposta = perguntar_groq(pergunta, st.session_state['contexto'])
        st.markdown("### Resposta:")
        st.write(resposta)
