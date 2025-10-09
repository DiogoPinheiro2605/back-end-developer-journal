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
        'id': 1,
        'name': "Paul",
        'skill_level': "Pleno",
        'activate': False,
    }
]