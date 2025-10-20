# app.py

from flask import Flask, request, jsonify
import os
import sys 
from dotenv import load_dotenv

# 💡 PATH FIX 💡
# Adds the project root directory to the Python search path (sys.path)
# This is crucial for absolute imports like 'from Agents.Excel.excel_agent import...'
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# ------------------

load_dotenv()
app = Flask(__name__)

# The Python environment can now resolve absolute imports:
# Remember, if you are using the Router, you should import the mother_agent function instead:
# from Agents.mother_agent import process_query 

# If testing the Excel Agent directly:
from Agents.Excel.excel_agent import analyze_data 

@app.route('/', methods=['GET'])
def home():
    """Simple test endpoint to check if the API is running."""
    return "LLM Excel Agent API is online! Send questions to /analyze_excel."

@app.route('/analyze_excel', methods=['POST'])
def analyze():
    """
    Endpoint to receive the user's question and call the LLM Agent.
    """
    try:
        # Receive JSON data from the request
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "The request must contain a 'question' field."}), 400
            
        user_question = data['question']
        
        print(f"-> Received Question: {user_question}")
        
        # Call the LLM Agent's analysis function
        llm_response = analyze_data(user_question)
        
        # Return the LLM response in JSON format
        return jsonify({
            "question": user_question,
            "answer": llm_response
        })

    except Exception as e:
        print(f"Internal Error: {e}")
        return jsonify({"error": f"An internal API error occurred: {e}"}), 500

if __name__ == '__main__':
    # Define port 5000 to run the application
    # Use 'debug=True' to auto-restart after code changes
    app.run(debug=True, port=5000)
