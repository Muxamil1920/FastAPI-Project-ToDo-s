from ..routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": 'Learn the Code',
        "description": 'Need To learn everyday',
        "complete": False,
        "id": 1,
        "priority": 2,
        "owner_id": 1
    }]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/read_todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": 'Learn the Code',
        "description": 'Need To learn everyday',
        "complete": False,
        "id": 1,
        "priority": 2,
        "owner_id": 1
    }

def test_read_one_authenticate_not_found(test_todo):
    response = client.get("todos/read_todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"Todo Not Found"}



def test_create_todo(test_todo):
    request_data = {
        "title": 'new todo',
        "description": 'new todo description',
        "complete": False,
        "priority": 3,
    }

    response = client.post("todos/create_todo", json = request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")

def test_update_todo(test_todo):
    request_data = {
        'title': 'New title updated to test put todo',
        'description': 'Need To learn everyday',
        'complete': False,
        'priority': 2,
        }

    response = client.put("todos/update_todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'New title updated to test put todo'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'New title updated to test put todo',
        'description': 'Need To learn everyday',
        'complete': False,
        'priority': 2,
    }

    response = client.put("todos/update_todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo Not Found'}


def test_delete_todo(test_todo):
    response = client.delete("todos/delete_todo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("todos/delete_todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not Found'}











