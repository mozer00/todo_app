from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate

#camada de serviço responsável pelas regras de negócio
#atua como intermediária entre a API e o acesso a dados (repository)

def get_task_by_id(db: Session, task_id: int) -> Task:
    #busca a tarefa na camada de persistência
    task = task_repository.get_by_id(db, task_id)

    #se nao encontrar a tarefa, repository retorna none
    #service converte isso em um erro http compreensível
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com id {task_id} não foi encontrada"
        )
    return task


def get_all_tasks(db: Session, skip: int=0, limit: int=100) -> list[Task]:
    
    #retorna lista de tarefas com suporte a paginação (skip/limit)
    return task_repository.get_all(db, skip=skip, limit=limit)     



def create_task(db: Session, task_data: TaskCreate) -> Task:

    #pede ao repository para criar a tarefa
    return task_repository.create(db, task_data)


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:

    #garante que a tarefa existe ou lança erro 404
    task = get_task_by_id(db, task_id)

    #regra de negócio: tarefas concluídas nao podem ser editadas para manter consistencia
    if task.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível editar uma tarefa já concluída"
        )
    
    return task_repository.update(db, task, task_data)


def delete_task(db: Session, task_id: int) -> None:

    #garante que a tarefa existe antes de realizar a remoção
    task = get_task_by_id(db, task_id)
    
    task_repository.delete(db, task)
    