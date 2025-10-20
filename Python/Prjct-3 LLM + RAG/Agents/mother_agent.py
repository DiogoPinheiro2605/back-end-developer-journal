# Agents/Excel/excel_agent.py

import os
import pandas as pd
from langchain_community.llms import Ollama
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from Agents.Excel.excel_reader import load_excel_data 


def create_excel_agent(df: pd.DataFrame):
    """
    Creates and configures the Pandas DataFrame Analysis Agent using Ollama (llama3).
    """
    if df is None:
        return None
        
    # 1. Configure the LLM to use Ollama (Local Model)
    try:
        llm = Ollama(
            model="llama3", # Ensure this model is pulled in your Ollama setup
            temperature=0  
        )
        print("✅ LLM (Ollama) successfully initialized.")
    except Exception as e:
        # If Ollama is installed but not running, this error will occur.
        print(f"❌ ERROR initializing Ollama. Check if the service is running: {e}")
        return None
        
    # 2. Create the Pandas Agent
    excel_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True, 
        handle_parsing_errors=True,
        
        # 🚨 ESSENTIAL FIX: Allows execution of the LLM-generated Pandas code
        allow_dangerous_code=True, 
        
        # 💡 ROBUST PREFIX FOR OLLAMA (to prevent error loops) 💡
        prefix="""
You are a specialist Pandas data analyst. Your sole objective is to analyze the DataFrame 'df' (which contains data from an Excel file).

You only have access to one tool: 'python_repl_ast'. Use it to generate Python/Pandas code that solves the user's question.

Strictly follow this reasoning and action format:

Thought: I must analyze the DataFrame 'df' to find the information.
Action: python_repl_ast
Action Input: [THE PYTHON/PANDAS CODE TO SOLVE THE QUESTION HERE]

If the action's observation is an error, generate a new corrected Action Input. 
If the observation contains the final answer, use it to formulate the final response.
""",
    )
    
    return excel_agent

def analyze_data(question: str):
    """
    Entry point to load data and query the LLM agent.
    This function is used by the Mother Agent as a Tool.
    """
    # 1. Load the data using the corrected function
    df = load_excel_data()
    
    # 2. Create the Agent with the DataFrame and Ollama
    agent = create_excel_agent(df)
    
    if agent is None:
        return "Sorry, I could not initialize the data analysis system with Ollama."
    
    # 3. Invoke the Agent with the question
    print(f"\n🧠 LLM AGENT (Ollama): Processing question: '{question}'...")
    
    try:
        # The agent receives the question from the Mother Agent
        response = agent.invoke({"input": question})
        return response.get("output", "Could not get a response from the agent.")
    except Exception as e:
        return f"An error occurred during analysis: {e}"
