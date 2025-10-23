
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from Extras.Connection import SessionLocal, Cliente 
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Dict, Any



def get_all_clients() -> List[Dict[str, Any]]:
    """
    Tool function to retrieve all client records from the database (READ).
    
    Returns:
        List[Dict[str, Any]]: A list of clients, where each client is a dictionary.
    """
    session: Session = SessionLocal()
    clients_list = []
    
    try:
        # 1. READ: Seleciona todos os clientes da tabela.
        # Usa .all() para obter todos os resultados.
        clients = session.scalars(select(Cliente)).all()
        
        # 2. Processamento: Converte cada objeto Cliente em um dicionário.
        for client in clients:
            # Converte o objeto do modelo SQLAlchemy em um dicionário
            client_dict = {
                # Mapeia os atributos do modelo para chaves do dicionário
                "id": client.id,
                "nome": client.nome,
                "email": client.email,
                "telefone": client.telefone,
                "morada": client.morada,
                "data_registo": str(client.data_registo) if client.data_registo else None,
                "ultima_compra": str(client.ultima_compra) if client.ultima_compra else None,
                "valor_gasto": float(client.valor_gasto) if client.valor_gasto else 0.0,
                "interesse": client.interesse,
                "notas": client.notas,
            }
            clients_list.append(client_dict)
            
        return clients_list
        
    except Exception as e:
        print(f"Error reading all clients: {e}")
        # Em caso de erro, retorna uma lista vazia ou levanta o erro (neste caso, retorna a lista vazia para simplificar o JSON).
        return []
        
    finally:
        session.close()


def get_client_by_id_or_email(identifier: str) -> Dict[str, Any]:
    """
    Tool function to retrieve a single client by ID or Email (READ).
    
    Args:
        identifier (str): The client's ID (integer string) or Email.
        
    Raises:
        NoResultFound: If no client matches the identifier.
    
    Returns:
        Dict[str, Any]: A dictionary representing the found client.
    """
    session: Session = SessionLocal()
    
    try:
        # Tenta converter o identificador para inteiro para buscar por ID
        try:
            client_id = int(identifier)
            # 1. READ by ID
            stmt = select(Cliente).filter(Cliente.id == client_id)
        except ValueError:
            # Se não for um ID, assume que é um Email
            # 2. READ by Email
            stmt = select(Cliente).filter(Cliente.email == identifier)
            
        # Usa .one() para garantir que levanta NoResultFound se não encontrar
        client = session.scalars(stmt).one()
        
        # 3. Processamento: Converte o objeto Cliente em um dicionário
        client_dict = {
            "id": client.id,
            "nome": client.nome,
            "email": client.email,
            "telefone": client.telefone,
            "morada": client.morada,
            "data_registo": str(client.data_registo) if client.data_registo else None,
            "ultima_compra": str(client.ultima_compra) if client.ultima_compra else None,
            "valor_gasto": float(client.valor_gasto) if client.valor_gasto else 0.0,
            "interesse": client.interesse,
            "notas": client.notas,
        }
        return client_dict
        
    except Exception as e:
        # O routes.py irá capturar NoResultFound e retornar 404
        # Outras exceções são tratadas aqui ou re-levantadas.
        session.rollback()
        raise e 
        
    finally:
        session.close()
