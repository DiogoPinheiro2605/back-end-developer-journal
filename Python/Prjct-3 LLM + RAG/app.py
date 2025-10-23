from flask import Flask
import os
import sys 
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

load_dotenv()
app = Flask(__name__)

from routes import clients_bp

app.register_blueprint(clients_bp) 

@app.route('/', methods=['GET'])
def root_home():
    """Rota inicial da aplicação, acessível em http://localhost:8000/."""
    return "LLM Agent System Root. See API routes starting at /api/."


if __name__ == '__main__':

    app.run(debug=True, port=8000)