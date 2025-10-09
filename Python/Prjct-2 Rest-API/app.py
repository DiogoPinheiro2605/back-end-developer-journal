#Objectives
# i will use flask
#Create one API where i can:
    #Search for a list of agents
    #Search for a specific agent
    #Edit a agent
    #Dele a agent
#If i can do that whitout a lot of trouble i want to go futher and
    # i want to implement notification, so i can know everytime an agent
    # is deleted, editer or add

#localhost/agents (GET)
#localhost/agents/id (GET)
#localhost/agent/id (PUT)
#localhost/agent/id (DELETE)

from flask import Flask, jsonify, request

app = Flask(__name__)

agents =[
    {
        'id': 1,
        'name': "Diogo",
        'skill_level': "Junior",
        'activate': True,
    },
    {
        'id': 2,
        'name': "John",
        'skill_level': "Senior",
        'activate': True,
    },
    {
        'id': 3, 
        'name': "Paul",
        'skill_level': "Pleno",
        'activate': False,
    }
]

@app.route("/agents",methods=["GET"])
def Get_Agents():
    return jsonify(agents)

@app.route("/agents/<int:id>",methods=["GET"])
def Agent_by_id(id):
    for agent in agents:
        if agent.get("id") == id:
            return jsonify(agent)
          
@app.route("/agents/<int:id>",methods=["PUT"])
def Edit_Agent(id):
    NewInformation = request.get_json()
    for index,agent in enumerate(agents):
        if agent.get("id") == id:
            agents[index].update(NewInformation)
            return jsonify(agents[index])

@app.route("/agents",methods=["POST"])
def Add_agent():
    new_agent = request.get_json()
    agents.append(new_agent)

    return jsonify(agents)

@app.route("/agents/<int:id>",methods=["DELETE"])
def Delete_agent(id):
    for agent in agents:
        if agent.get("id") == id:
            agents.remove(agent)

    return jsonify(agents)

app.run(port=5000,host="localhost",debug=True)