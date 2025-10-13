import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

def agent_ai_response(agent, user_message):
    """
    Envia a mensagem do utilizador para o modelo LLaMA via Ollama.
    """
    prompt = f"""
You are {agent['name']}, a {agent['job']} agent.
Skill level: {agent['skill_level']}
Personality: {agent['personality']}.

User message: "{user_message}"

Respond naturally and concisely.
"""

    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": True  # <- importante: ativa o streaming (resposta vem em partes)
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        # Como o Ollama envia várias linhas JSON, precisamos ler todas
        full_reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    if "message" in json_data and "content" in json_data["message"]:
                        full_reply += json_data["message"]["content"]
                except json.JSONDecodeError:
                    continue  # ignora pedaços incompletos

        return full_reply.strip() if full_reply else "Sem resposta do modelo."

    except requests.exceptions.RequestException as e:
        return f"Erro ao comunicar com o Ollama: {e}"
