import requests
import json

def ask_llm(prompt: str, model: str = "llama3") -> str:
    url = "http://127.0.0.1:11434/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False 
    }
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        return f"Erro HTTP {resp.status_code}: {resp.text}"
    try:
        data = resp.json()
        if "completion" in data:
            return data["completion"]
        elif "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        else:
            return "Erro: resposta vazia do modelo."
    except Exception as e:
        return f"Erro ao ler resposta do LLM: {str(e)}"
