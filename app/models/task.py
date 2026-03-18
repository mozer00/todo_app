from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Task(Base):
    #nome da tabela no banco
    __tablename__ = "tasks"

    #colunas da tabela
    #id é a chave primária, auto-incrementada e indexada para melhorar a performance das consultas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    #titulo é uma string de até 200 caracteres, não pode ser nula
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    #descriçao é uma string de até 500 caracteres, preenchimento opcional (pode ser nulo)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    #tarefa completa ou não, valor booleano, padrão é False (não completa) e não pode ser nulo
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    #datetime captura a hora exata de criação da tarefa
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    #toda vez que houver uma atualização na tarefa, onupdate é executado
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    #printar a task
    def __repr__(self) -> str:
        return f"<Task id={self.id} title='{self.title}' completed={self.is_completed}>"