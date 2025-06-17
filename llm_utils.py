import requests

def perguntar_para_ia(pergunta, contexto):
    prompt = f"""
Você é um assistente da Coram Deo. Baseie sua resposta **apenas** no conteúdo abaixo:

Contexto:
{contexto}

Pergunta: {pergunta}
Resposta:
    """
    # Usando API Groq com LLaMA 3 (exemplo)
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"Erro: {res.status_code} - {res.text}"
