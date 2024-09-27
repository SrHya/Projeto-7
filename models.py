from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import os

# Definir o caminho do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'users.db')

# Criar o engine do SQLAlchemy
engine = create_engine(f'sqlite:///{database_path}', echo=True)

# Declarar a base para as classes do modelo
Base = declarative_base()

# Definir a classe User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)
