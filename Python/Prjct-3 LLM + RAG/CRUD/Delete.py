
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from Extras.Connection import SessionLocal, Cliente 
from sqlalchemy.orm.exc import NoResultFound
# crud_delete.py

def remove_client_by_email(client_email: str) -> str:
    """Tool to remove a client from the database using their email (DELETE)."""
    session: Session = SessionLocal()
    try:
        # 1. READ: Find the client by 'email'
        client = session.scalars(select(Cliente).filter(Cliente.email == client_email)).one()
        
        client_name = client.nome
        
        # 2. DELETE: Prepare and execute the deletion
        session.delete(client)
        session.commit() 
        
        return f"Success! Client '{client_name}' (Email: {client_email}) removed from the database."
    except NoResultFound:
        return f"Error: Client with email '{client_email}' not found."
    except Exception as e:
        session.rollback()
        return f"Error while removing client: {str(e)}"
    finally:
        session.close()