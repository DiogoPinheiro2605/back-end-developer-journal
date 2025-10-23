
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from Extras.Connection import SessionLocal, Cliente 

# Placeholder for the actual email sending function
def send_email(recipient: str, client_name: str, new_interest: str) -> str:
    """Simulated email sending function."""
    print(f"SIMULATED EMAIL SENT: Client: {client_name}, Subject: New interest in {new_interest}")
    return f"Email notification SIMULATED for {recipient} about '{new_interest}'."


def update_client_interest(client_name: str, new_interest: str) -> str:
    """
    Tool to update the client's 'interesse' and trigger the email notification (UPDATE).
    """
    session: Session = SessionLocal()
    
    # Map input variables (English) to model attributes (Portuguese)
    interesse_input = new_interest
    
    try:
        # 1. READ: Find the client by 'nome'
        client = session.scalars(select(Cliente).filter(Cliente.nome == client_name)).one()
        
        old_interest = client.interesse
        
        if old_interest != interesse_input:
             # 2. UPDATE: Modify the Python object attribute
             client.interesse = interesse_input
             session.commit() # Executes the UPDATE command
             
             # 3. EMAIL TRIGGER
             email_status = send_email(client.email, client.nome, interesse_input)
             
             return f"Success! Client '{client_name}' interest updated to '{interesse_input}'. {email_status}"
        
        return f"Action unnecessary: Client '{client_name}' interest was already '{old_interest}'."
    
    except NoResultFound:
        return f"Error: Client '{client_name}' not found in the database."
    except Exception as e:
        session.rollback()
        return f"Error during update: {str(e)}"
    finally:
        session.close()