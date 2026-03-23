from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service


#camada de entrada da aplicação (HTTP)
#responsável por receber requisições, validar dados e delegar para a camada de serviço


#prefix = todas as rotas terão /tasks na frente automaticamente
#tags = agrupa os endpoints na documentação /docs
router = APIRouter(prefix="/task", tags=["Tasks"])


@router.get(
    "/",
    response_model=list[TaskResponse],  #define o schema de resposta (serialização)
    status_code=status.HTTP_200_OK
)
def list_tasks(
    skip: int = 0,
    limit: int = 100,               #parâmetros de paginação via query string: GET /tasks?skip=0&limit=10
    db: Session = Depends(get_db)   #injeção da sessão do banco via dependency
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
    task_data: TaskCreate,  #fastapi lê o body json e valida com taskcreate
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
    task_data: TaskUpdate,   #body json validado com taskupdate
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
    task_service.delete_task(db, task_id)  #204 indica sucesso sem conteúdo de resposta