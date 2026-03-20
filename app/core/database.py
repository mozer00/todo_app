from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# conexao com o banco de dados
DATABASE_URL = "sqlite:///./todo.db"

# fastapi usa multi threads, sqlite só permite uso na thread que criou, entao tem que tratar
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#autocommit/autoflush=false para controlar quando salvar e para o sqlalchemy nao enviar sql pro banco antes do commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#classe base, todo model vai herdar dela
class Base(DeclarativeBase):
    pass

#abre e fecha a conexao com o banco de dados, usando o yield para criar um gerenciador de contexto
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()