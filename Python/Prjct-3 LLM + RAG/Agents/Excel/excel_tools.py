
from langchain.tools import tool
# Import the main analysis function from your existing agent file
from excel_agent import analyze_data 

@tool
def excel_analyzer(question: str) -> str:
    """
    Use this tool ONLY to answer questions that require data analysis 
    on the Excel file, such as calculations, averages, sums, counts, or filtering 
    based on columns like 'Gasto', 'Morada', 'Interesse', etc.
    The input must be the user's complete question.
    """
    # This calls your pre-configured Excel Agent and returns its output
    return analyze_data(question)

# List of tools for the Mother Agent to use
available_tools = [excel_analyzer]