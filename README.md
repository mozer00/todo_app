# Todo API

Projeto de estudo desenvolvido para praticar a construção de uma API REST do zero,
passando por todas as camadas de uma aplicação: banco de dados, regras de negócio,
endpoints e testes automatizados.

## Sobre o projeto

A ideia foi construir um gerenciador de tarefas simples, mas com uma arquitetura
organizada em camadas — algo que eu não sabia fazer antes de começar.
O foco foi entender como as peças se conectam: o FastAPI recebe a requisição,
o service aplica as regras, o repository fala com o banco, e o Pydantic garante
que os dados estejam corretos em cada etapa.

## Tecnologias utilizadas

- **Python 3.14**
- **FastAPI** — framework para construção da API
- **SQLAlchemy** — ORM para comunicação com o banco de dados
- **Alembic** — controle de versão do banco (migrations)
- **SQLite** — banco de dados local
- **Pydantic** — validação dos dados de entrada e saída
- **Pytest** — testes automatizados
- **Ruff** — linting e formatação do código

## Arquitetura

O projeto segue uma arquitetura em camadas, onde cada parte tem uma responsabilidade única:
```
app/
├── api/v1/routes/     # endpoints — recebe as requisições HTTP
├── core/              # configuração do banco de dados
├── models/            # definição das tabelas (SQLAlchemy)
├── schemas/           # contratos de entrada e saída (Pydantic)
├── repositories/      # queries no banco de dados
└── services/          # regras de negócio
```

## Como rodar localmente

**Pré-requisitos:** Python 3.10+
```bash
# Clone o repositório
git clone https://github.com/mozer00/todo_app.git
cd todo_app

# Crie e ative o ambiente virtual
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Crie as tabelas no banco
alembic upgrade head

# Inicie o servidor
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`

## Documentação

O FastAPI gera uma documentação interativa automaticamente.
Acesse `http://127.0.0.1:8000/docs` para visualizar e testar todos os endpoints
pelo navegador, sem precisar de nenhuma ferramenta externa.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/task/` | Lista todas as tarefas |
| GET | `/api/v1/task/{id}` | Busca uma tarefa pelo id |
| POST | `/api/v1/task/` | Cria uma nova tarefa |
| PATCH | `/api/v1/task/{id}` | Edita uma tarefa existente |
| DELETE | `/api/v1/task/{id}` | Remove uma tarefa |

**Regra de negócio:** tarefas marcadas como concluídas não podem ser editadas.

## Testes
```bash
# Roda todos os testes
pytest

# Com detalhes de cada teste
pytest -v
```

12 testes cobrindo os principais cenários de uso: criação, listagem, busca,
edição e remoção — tanto os caminhos de sucesso quanto os de erro.

## O que aprendi

- Como estruturar um projeto Python com separação de responsabilidades
- Como o SQLAlchemy converte objetos Python em comandos SQL
- A diferença entre models (banco) e schemas (API)
- Como o Alembic versiona mudanças no banco de dados
- Como o FastAPI injeta dependências automaticamente com `Depends`
- Como escrever testes com banco isolado usando pytest e fixtures