import requests
import streamlit as st

def perguntar_para_ia(pergunta, contexto):
    prompt = f"""
Você é um assistente da Coram Deo. Baseie sua resposta **apenas** no conteúdo abaixo:

Contexto:
{contexto}

Pergunta: {pergunta}
Resposta:
    """

    headers = {
        "Authorization": f"Bearer {st.secrets['groq']['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 500
    }

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)

    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Erro: {res.status_code} - {res.text}"
