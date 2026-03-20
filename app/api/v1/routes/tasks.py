from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service


#prefix = todas as rotas terão /tasks na frente automaticamente
#tags = agrupa os endpoints na documentação /docs
router = APIRouter(prefix="/task", tags=["Tasks"])


@router.get(
    "/",
    response_model=list[TaskResponse],  # fala pro fastapi como serializar a resposta
    status_code=status.HTTP_200_OK
)
def list_tasks(
    skip: int = 0,
    limit: int = 100,               #parâmetros de query: GET /tasks?skip=0&limit=10
    db: Session = Depends(get_db)   #fastapi injeta a session automaticamente
):
    return task_service.get_all_tasks(db, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def get_task(
    task_id: int,    #fastapi pega do path: GET /tasks/1
    db: Session = Depends(get_db)
):
    return task_service.get_task_by_id(db, task_id)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED  #201 = criado com sucesso
)
def create_task(
    task_data: TaskCreate,  #fastapi le o body json e valida com taskcreate
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, task_data)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,   #body json validade com taskupdate
    db: Session = Depends(get_db)
):
    return task_service.update_task(db, task_id, task_data)

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT   #204 = sucesso sem corpo de resposta

)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task_service.delete_task(db, task_id)  #nao tem return pq 204 nao tem corpo, entao nao precisa retornar nada