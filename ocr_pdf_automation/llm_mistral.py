import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

def analisar_texto_com_mistral(texto: str) -> str:
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "Você é um assistente que extrai informações de documentos."},
            {"role": "user", "content": f"Extraia os principais campos do documento abaixo e devolva em JSON:\n\n{texto}"}
        ],
        "temperature": 0.2
    }

    resp = requests.post(MISTRAL_URL, headers=headers, json=payload, timeout=120)

    if resp.status_code != 200:
        raise Exception(resp.text)

    return resp.json()["choices"][0]["message"]["content"]