from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



#base = campo compartilhado entre create e response
class TaskBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        examples=["Leitura relaxante antes de dormir"]
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        examples=["Ler ao menos 5 minutos de uma ficção para desligar das telas."]
    )


#create (herda title e description do taskbase, nao tem id, iscompleted, created_at, updated_at)
class TaskCreate(TaskBase):
    pass


#update (nao herda do taskbase, pois o usuário edita o que quiser e é opcional)
class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        examples=["Triagem de E-mails"]
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
        examples=["Responder apenas o que leva menos de 2 minutos; o resto vira tarefa para depois."]
    )
    is_completed: bool | None = Field(
        default=None,
        examples=[True]
    )


#response = o que é devolvido para o cliente, herda title e description do taskbase
class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    #usado para converter um obj sqlalchemy(task) em um schema(taskresponse)
    #sqlalchemy retorna objetos python, nao dicionarios
    #from_attributes=True fala pro pydantic: leia os atributos do objeto
    model_config = ConfigDict(from_attributes=True)
    