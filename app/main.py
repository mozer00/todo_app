from fastapi import FastAPI
from app.api.v1.router import api_router


#instancia a aplicacao com metadados para a documentação
app = FastAPI(
    title="Todo API",
    description="API de gerenciamento de tarefas",
    version="1.0.0"
)


#registra todas as rotas da v1
app.include_router(api_router)


#rota raiz para verificar se a api está no ar
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Todo API está funcionando"}