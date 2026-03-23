#AAA pattern = arrange-act-assert

def test_create_task_success(client):
    #arrange = prepara os dados de entrada
    payload = {
        "title": "Organizar a sala",
        "description": "Guardar o que tá espalhado pelo sofá e deixar o ambiente em ordem."
    }

    #act = executa a açao(request)
    response = client.post("/api/v1/task/", json=payload)

    #assert = valida o resultado
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Organizar a sala"
    assert data["description"] == "Guardar o que tá espalhado pelo sofá e deixar o ambiente em ordem."
    assert data["is_completed"] == False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_empty_title(client):
    #titulo vazio = com espaço em branco
    payload = {"title": "", "description": "qualquer coisa"}
    response = client.post("/api/v1/task/", json=payload)
    assert response.status_code == 422


def test_create_task_missing_title(client):
    #sem titulo
    payload = {"description": ""}
    response = client.post("/api/v1/task/", json=payload)
    assert response.status_code == 422


def test_list_tasks_empty(client):
    #banco vazio retorna lista vazia
    response = client.get("/api/v1/task/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_task_with_data(client):
    #cria multiplas tarefas e verifica se sao retornadas na listagem
    client.post("/api/v1/task/", json={"title": "Tarefa 1"})
    client.post("/api/v1/task/", json={"title": "Tarefa 2"})
    
    response = client.get("/api/v1/task/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id_success(client):
    #cria e busca pelo id retornado
    created = client.post("/api/v1/task/", json={"title":"Retorno do id:"})
    task_id = created.json()["id"]

    response = client.get(f"/api/v1/task/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Retorno do id:"


def test_get_task_by_id_not_found(client):
    #deve retornar 404 quando a tarefa nao existe
    response = client.get("/api/v1/task/99999")
    assert response.status_code == 404


def test_update_task_success(client):
    #cria e edita apenas o titulo
    created = client.post("/api/v1/task/", json={"title": "Titulo original"})
    task_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/task/{task_id}",
        json={"title": "Titulo atualizado"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Titulo atualizado"


def test_update_completed_task_fails(client):
    #regra de negocio: tarefas concluídas nao podem ser editadas
    created = client.post("/api/v1/task/", json={"title": "Concluir esta"})
    task_id = created.json()["id"]

    #marca a tarefa como concluida
    client.patch(
        f"/api/v1/task/{task_id}",
        json={"is_completed": True}
        )

    #tenta editar e deve retornar 400 pois ja esta concluido
    response = client.patch(
        f"/api/v1/task/{task_id}",
        json={"title": "Nova tentativa"}

    )
    assert response.status_code == 400


def test_update_task_not_found(client):
    response = client.patch("/api/v1/task/99999", json={"title": "x"})
    assert response.status_code == 404


def test_delete_task_success(client):
    created = client.post("/api/v1/task/", json={"title": "Deletar esse"})
    task_id = created.json()["id"]

    response = client.delete(f"/api/v1/task/{task_id}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/task/{task_id}")
    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/api/v1/task/99999")
    assert response.status_code == 404