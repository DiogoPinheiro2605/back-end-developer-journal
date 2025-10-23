# crud_create.py
from sqlalchemy.orm import Session # Importa Session do SQLAlchemy
from datetime import date
from sqlalchemy import select
from Extras.Connection import SessionLocal, Cliente

def add_new_client(name: str, email: str, interest: str, phone: str = None, address: str = None) -> str:
    """
    Tool function to add a new client to the database (CREATE).
    It uses the Portuguese column names defined in the Cliente model.
    """
    session: Session = SessionLocal()
    
    # ⚠️ Map input variables (English) to model attributes (Portuguese)
    nome_input = name
    interesse_input = interest
    telefone_input = phone
    # morada_input = address # Use if you add 'morada' to the function signature
    
    try:
        # 1. VERIFICATION (READ) - Checks for unique email
        if session.execute(select(Cliente).filter(Cliente.email == email)).scalar_one_or_none():
            return f"Failure: Client with email {email} already exists."
            
        # 2. CREATION (CREATE) - Using Portuguese attribute names
        new_client = Cliente(
            nome=nome_input, 
            email=email, 
            interesse=interesse_input, 
            telefone=telefone_input,
            # morada=morada_input, # Uncomment if included
            data_registo=date.today()
        )
        session.add(new_client) 
        session.commit()          
        
        return f"Success! Client '{nome_input}' added. ID: {new_client.id}"
    except Exception as e:
        session.rollback()        # Rolls back if anything fails
        return f"Error: {str(e)}"
    finally:
        session.close()