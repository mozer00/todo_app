from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

#camada responsável pela persistência de dados (CRUD no banco)
#não deve conter regras de negócio


def get_by_id(db: Session, task_id: int) -> Task | None:

    #select(Task) → gera "SELECT * FROM tasks"
    #where(Task.id == task_id) → gera "WHERE id = :task_id"
    statement = select(Task).where(Task.id == task_id)
    #scalars() → diz ao SQLAlchemy para retornar objetos Task, não tuplas
    #first() → pega o primeiro resultado ou None se não encontrar
    return db.scalars(statement).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:

    #aplica paginaçao via offset (skip) e limit
    statement = select(Task).offset(skip).limit(limit)
    #all() → retorna uma lista com todos os resultados
    return list(db.scalars(statement).all())

def create(db: Session, task_data: TaskCreate) -> Task:

    #model_dump() converte o schema pydantic em dicionário python
    # ** desempacota o dicionário como argumentos nomeados
    #resultado: Task(title="...", description="...")
    db_task = Task(**task_data.model_dump())

    db.add(db_task)     #adiciona o objeto na session (ainda não salva)
    db.commit()         #envia o INSERT para o banco e confirma
    db.refresh(db_task) #atualiza o objeto com os dados gerados pelo banco
                        #(id, created_at, updated_at que o banco preencheu)
    return db_task

def update(db: Session, db_task: Task, task_data: TaskUpdate) -> Task:

    #model_dump(exclude_unset=True) retorna apenas os campos que o
    #usuario alterou, ignorando os que ficaram como none por padrão
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_task, field, value)    #atualiza os campos do objeto        
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete(db: Session, db_task: Task) -> None:
    
    #remove a entidade do banco de dados
    db.delete(db_task)  #seleciona qual objeto será removido
    db.commit()         #envia e confirma a exclusao
