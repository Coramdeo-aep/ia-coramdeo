from supabase import create_client
import streamlit as st

def get_supabase_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def buscar_contexto_documentos():
    supabase = get_supabase_client()
    resposta = supabase.table("documentos").select("conteudo").execute()
    documentos = resposta.data if resposta.data else []
    textos = [doc["conteudo"] for doc in documentos if "conteudo" in doc and doc["conteudo"]]
    return "\n".join(textos)
