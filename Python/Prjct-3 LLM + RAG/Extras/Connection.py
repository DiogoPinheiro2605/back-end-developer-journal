# database.py

from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER = 'root'
PASSWORD = '1234'
HOST = 'localhost'
DATABASE_NAME = 'db_python' 

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    telefone = Column(String(50))
    morada = Column(String(255))
    
    data_registo = Column(Date)
    ultima_compra = Column(Date)
    valor_gasto = Column(DECIMAL(10, 2))
    
    interesse = Column(String(255))
    notas = Column(Text)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)