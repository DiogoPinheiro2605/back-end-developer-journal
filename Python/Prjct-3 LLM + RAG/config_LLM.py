import requests
import json

# Endereços padrão
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"   # Para uso direto no Ollama
FLASK_URL = "http://127.0.0.1:8000/api/chat"      # Para uso via Flask (se tiver rota que chama o LLM)

def ask_llm(prompt: str, model: str = "llama3", use_flask: bool = False) -> str:
    """
    Envia o prompt para o Ollama (ou API Flask) e retorna a resposta.
    Se 'use_flask=True', envia via Flask.
    """
    try:
        url = FLASK_URL if use_flask else OLLAMA_URL

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code != 200:
            return f"Erro HTTP {response.status_code}: {response.text}"

        # Tenta ler o JSON retornado
        try:
            data = response.json()
        except json.JSONDecodeError:
            return f"Erro: resposta inválida do servidor ({url})."

        # Ollama pode devolver diferentes formatos
        if "completion" in data:
            return data["completion"]
        elif "message" in data and isinstance(data["message"], dict):
            return data["message"].get("content", "Erro: resposta vazia do modelo.")
        elif "output" in data:
            return data["output"]
        elif isinstance(data, list) and len(data) > 0:
            return data[-1].get("message", {}).get("content", "Erro: resposta vazia do modelo.")
        else:
            return "Erro: formato de resposta não reconhecido."

    except requests.exceptions.ConnectionError:
        return f"Erro: não foi possível conectar a {url}. Verifica se o Ollama (ou Flask) está a correr."
    except Exception as e:
        return f"Erro ao comunicar com LLM: {str(e)}"
