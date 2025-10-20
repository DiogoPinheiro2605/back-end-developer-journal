# app.py


from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from Agents.excel_agent import analyze_data 

# Carrega variáveis de ambiente (como a chave API) de um arquivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Endpoint de teste simples para verificar se a API está a funcionar."""
    return "API do Agente Excel LLM está online! Envie perguntas para /analyze_excel."

@app.route('/analyze_excel', methods=['POST'])
def analyze():
    """
    Endpoint para receber a pergunta do utilizador e chamar o Agente LLM.
    """
    try:
        # Recebe os dados JSON da requisição
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "A requisição deve conter um campo 'question'."}), 400
            
        user_question = data['question']
        
        print(f"-> Pergunta Recebida: {user_question}")
        
        # Chama a função de análise do Agente LLM
        llm_response = analyze_data(user_question)
        
        # Retorna a resposta do LLM em formato JSON
        return jsonify({
            "question": user_question,
            "answer": llm_response
        })

    except Exception as e:
        print(f"Erro interno: {e}")
        return jsonify({"error": f"Ocorreu um erro interno na API: {e}"}), 500

if __name__ == '__main__':
    # Define a porta 5000 para rodar a aplicação
    # Use 'debug=True' para reiniciar automaticamente após alterações no código
    app.run(debug=True, port=5000)
