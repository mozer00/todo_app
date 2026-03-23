from fastapi import APIRouter
from app.api.v1.routes import tasks


#serve para agregar todas as rotas da versao 1 da api
#o main.py vai importar todas as rotas da v1, por aqui
#sem esse router agregador, o main teria que importar cada um arquivo de rota
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(tasks.router)