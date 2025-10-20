# Agents/excel_agent.py

import os
import pandas as pd
from langchain_community.llms import Ollama
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from Data.excel_reader import load_excel_data 


def create_excel_agent(df: pd.DataFrame):
    """
    Creates and configures the Pandas DataFrame Analysis Agent using Ollama.
    """
    if df is None:
        return None
        
    try:
        llm = Ollama(
            model="llama3",
            temperature=0  
        )
        print("✅ LLM (Ollama) successfully initialized.")
    except Exception as e:
        print(f"❌ ERROR initializing Ollama. Check if the service is running: {e}")
        return None
        
    # 2. Create the Pandas Agent
    excel_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        handle_parsing_errors=True,
        allow_dangerous_code=True,
        
        prefix="""
You are a specialist Pandas data analyst. Your sole objective is to analyze the DataFrame 'df' (which contains data from an Excel file).

You only have access to one tool: 'python_repl_ast'. Use it to generate Python/Pandas code that solves the user's question.

Strictly follow this reasoning and action format:

Thought: I must analyze the DataFrame 'df' to find the information.
Action: python_repl_ast
Action Input: [THE PYTHON/PANDAS CODE TO SOLVE THE QUESTION HERE]

If the action's observation is an error, generate a new corrected Action Input. 
If the observation contains the final answer, use it to formulate the final response.
"""
    )
    
    return excel_agent

def analyze_data(question: str):
    """
    Entry point to load data and query the LLM agent.
    """
    # 1. Load the data
    df = load_excel_data()
    
    # 2. Create the Agent with the DataFrame and Ollama
    agent = create_excel_agent(df)
    
    if agent is None:
        return "Sorry, I could not initialize the data analysis system with Ollama."
    
    # 3. Invoke the Agent with the question
    print(f"\n🧠 AGENT LLM (Ollama): Processing question: '{question}'...")
    
    try:
        response = agent.invoke({"input": question})
        return response.get("output", "Could not get a response from the agent.")
    except Exception as e:
        return f"An error occurred during analysis: {e}"

if __name__ == "__main__":
    test_question = "What is the average of the 'Valor Gasto (€)' column and what are the 3 most common 'Notas'?"
    response = analyze_data(test_question)
    print("\n=============================================")
    print(f"FINAL OLLAMA RESPONSE FOR THE QUESTION: {response}")
    print("=============================================")