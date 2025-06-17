from groq import Groq
from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def responder_pergunta(pergunta, contexto):
    prompt = f"""
Responda com base apenas no conteúdo a seguir:

{contexto}

Pergunta: {pergunta}
    """
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro: {e}"
