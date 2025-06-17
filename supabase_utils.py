from supabase import create_client
import streamlit as st

def get_supabase_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def buscar_contexto():
    supabase = get_supabase_client()
    data = supabase.table("ia_base").select("*").execute()
    registros = data.data if data.data else []
    textos = [r["conteudo"] for r in registros if "conteudo" in r]
    return "\n".join(textos)
