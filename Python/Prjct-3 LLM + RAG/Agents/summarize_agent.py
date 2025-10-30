import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

try:
    from config_LLM import ask_llm
except ImportError:
    def ask_llm(prompt):
        return "ERROR: config_LLM module not loaded."

def summarize_response(
    user_query: str, 
    context: str, 
    role_prompt: str
) -> str:
    """
    Constructs the final prompt combining the role, context, and query, 
    and sends it to the LLM for summarization/response generation.
    """

    final_prompt = f"""
{role_prompt}

Based ONLY on the context below to answer the question. If the answer is not in the context, respond: "The information you are looking for was not found in the database."

Context:
{context}

Question: {user_query}
"""
    
    return ask_llm(final_prompt)