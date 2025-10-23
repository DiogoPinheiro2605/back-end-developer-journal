# routes.py

from flask import Blueprint, request, jsonify
from sqlalchemy.orm.exc import NoResultFound
from pydantic import BaseModel, ValidationError, EmailStr
import json
from Agents.Excel.excel_agent import analyze_data
#CRUD
from CRUD.Create import add_new_client
from CRUD.Read import get_all_clients, get_client_by_id_or_email
from CRUD.Update import update_client_interest 
from CRUD.Delete import remove_client_by_email


clients_bp = Blueprint('clients_api', __name__, url_prefix='/api')

class ClientInput(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None
    morada: str | None = None
    interesse: str
    notas: str | None = None

@clients_bp.route("/clients", methods=["POST"])
def add_client_route():
    """Route para adicionar um novo cliente. Chama a ferramenta add_new_client."""
    try:

        data = ClientInput(**request.get_json())
    except ValidationError as e:

        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400

    # 2. Chama a função de CRUD (que interage com o SQLAlchemy)
    result = add_new_client(
        name=data.nome,
        email=data.email,
        interest=data.interesse,
        phone=data.telefone,
        address=data.morada
    )
    
    if "Success!" in result:
        # Retorna 201 (Created) em caso de sucesso
        return jsonify({"message": "Client added successfully", "result": result}), 201
    else:
        # Retorna 400 se a inserção falhar (ex: e-mail duplicado)
        return jsonify({"error": "Database insertion failed", "details": result}), 400

# B. READ (GET)
@clients_bp.route("/clients", methods=["GET"])
def get_all_clients_route():
    """Route para obter a lista de todos os clientes. Chama a ferramenta get_all_clients."""
    try:
        data = get_all_clients()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching clients: {str(e)}"}), 500

@clients_bp.route("/clients/<string:identifier>", methods=["GET"])
def get_single_client_route(identifier):
    """Route para obter um cliente por ID ou Email. Chama a ferramenta get_client_by_id_or_email."""
    try:
        client = get_client_by_id_or_email(identifier)
        return jsonify(client), 200
    except NoResultFound:
        return jsonify({"error": f"Client with ID/Email '{identifier}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error searching for client: {str(e)}"}), 500

# C. DELETE (DELETE)
@clients_bp.route("/clients/<string:client_email>", methods=["DELETE"])
def delete_client_route(client_email):
    """Route para remover um cliente pelo Email. Chama a ferramenta remove_client_by_email."""
    result = remove_client_by_email(client_email)
    
    if "Success!" in result:
        return jsonify({"message": "Client successfully removed", "result": result}), 200
    else:
        # Retorna 404 se o cliente não for encontrado para deletar
        return jsonify({"error": "Failed to remove client", "details": result}), 404

@clients_bp.route('/', methods=['GET'])
def home():
    """Simple test endpoint to check if the API is running."""

    return "LLM Agent API is online! Access CRUD routes at /api/clients or chat with the agent at /api/chat."

@clients_bp.route('/analyze_excel', methods=['POST'])
def analyze():
    """
    Endpoint para receber a questão do usuário e chamar o LLM Agent (Excel).
    Esta é a rota movida do app.py.
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "The request must contain a 'question' field."}), 400
            
        user_question = data['question']
        
        print(f"-> Received Question: {user_question}")
        
        # Chama a função do agente Excel
        llm_response = analyze_data(user_question)
        
        return jsonify({
            "question": user_question,
            "answer": llm_response
        })

    except Exception as e:
        print(f"Internal Error in Excel Agent: {e}")
        return jsonify({"error": f"An internal API error occurred: {e}"}), 500
    
@clients_bp.route("/chat", methods=["POST"])
def chat_with_agent_route():
    """
    Route principal. Recebe o prompt do usuário e o envia ao LLM Agent.
    O Agente decide se deve chamar uma TOOL (ex: update_client_interest) ou responder.
    """
    data = request.get_json()
    message = data.get("message")
    
    if not message:
        return jsonify({"error": "Chat message is required."}), 400

    # ⚠️ Integração real do LLM Agent (Descomentar e configurar)
    # try:
    #     response = agente_final.invoke({"input": message})
    #     
    #     return jsonify({
    #         "agent_response": response["output"],
    #         "agent_log": response["intermediate_steps"] # Passos que o agente usou
    #     }), 200
        
    # except Exception as e:
    #     return jsonify({"error": f"LLM Agent encountered an error: {str(e)}"}), 500
    
    # Resposta de placeholder (SIMULAÇÃO)
    if "update" in message.lower() or "muda o interesse" in message.lower():
        return jsonify({"agent_response": "Simulation: The LLM Agent identified a database update intention and would call the 'update_client_interest' Tool.", "message": message}), 200
    return jsonify({"agent_response": "Simulation: The LLM Agent will answer your query without calling a database tool.", "message": message}), 200

