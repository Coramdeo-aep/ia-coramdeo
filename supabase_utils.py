import requests
import json
from urllib.parse import quote
from config import SUPABASE_URL, SUPABASE_ANON_KEY, TABELA


def documento_existe(caminho):
    url = f"{SUPABASE_URL}/rest/v1/{TABELA}?caminho_arquivo=eq.{quote(caminho)}"
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}
    r = requests.get(url, headers=headers)
    return r.status_code == 200 and len(r.json()) > 0


def inserir_documento(nome, caminho, tipo, conteudo):
    url = f"{SUPABASE_URL}/rest/v1/{TABELA}"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "nome_arquivo": nome,
        "caminho_arquivo": caminho,
        "tipo": tipo,
        "conteudo": conteudo[:30000]
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return r.status_code == 201


def buscar_conteudos():
    url = f"{SUPABASE_URL}/rest/v1/{TABELA}?select=conteudo"
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return [item['conteudo'] for item in r.json()]
    return []
