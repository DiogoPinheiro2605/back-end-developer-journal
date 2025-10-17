# app.py
from flask import Flask, request, jsonify
from ai_utils import agent_ai_response

app = Flask(__name__)

# Base de agentes
agents = [
    {"id": 1, "name": "Mother-agent", "skill_level": "Senior", "activate": True, "job": "Sales", "personality": "helpful and guiding"},
    {"id": 2, "name": "John", "skill_level": "Senior", "activate": True, "job": "Marketing", "personality": "friendly and persuasive"},
    {"id": 3, "name": "Paul", "skill_level": "Junior", "activate": False, "job": "Calls", "personality": "shy but efficient"},
]

# --- Endpoints ---

@app.route("/agents", methods=["GET"])
def get_agents():
    return jsonify(agents)

@app.route("/agents/<int:id>", methods=["GET"])
def get_agent(id):
    agent = next((a for a in agents if a["id"] == id), None)
    if agent:
        return jsonify(agent)
    return jsonify({"error": "Agent not found"}), 404

@app.route("/agents/<int:id>", methods=["PUT"])
def edit_agent(id):
    data = request.get_json()
    agent = next((a for a in agents if a["id"] == id), None)
    if agent:
        agent.update(data)
        return jsonify(agent)
    return jsonify({"error": "Agent not found"}), 404

@app.route("/agents/<int:id>", methods=["DELETE"])
def delete_agent(id):
    agent = next((a for a in agents if a["id"] == id), None)
    if agent:
        agents.remove(agent)
        return jsonify({"message": "Agent deleted"})
    return jsonify({"error": "Agent not found"}), 404

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    agent_id = data.get("agent_id")
    message = data.get("message")
    
    agent = next((a for a in agents if a["id"] == agent_id), None)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404

    if agent["name"] == "Mother-agent":
        agent = agents[1]  # delega para John

    response_text = agent_ai_response(agent, message)
    return jsonify({"agent": agent["name"], "response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
