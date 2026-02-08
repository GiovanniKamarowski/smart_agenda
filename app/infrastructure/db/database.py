from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# URL de conexão com o banco SQLite local
# O arquivo será criado automaticamente na raiz do projeto com o nome smartagenda.db
DATABASE_URL = "sqlite:///./smartagenda.db"


# Engine é o componente responsável por conectar o SQLAlchemy ao banco
# check_same_thread=False é obrigatório no SQLite quando usado com FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# SessionLocal é uma fábrica de sessões do banco
# Cada request deve usar uma sessão separada para evitar conflitos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base é a classe base usada para criar os Models do SQLAlchemy
# Todos os models (EventoModel, LembreteModel, NotificacaoModel) herdam dela
Base = declarative_base()


def get_db():
    """
    Dependency do FastAPI para fornecer uma sessão do banco.

    Fluxo:
    - abre uma sessão
    - entrega para o endpoint/service
    - fecha automaticamente ao final da request
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
