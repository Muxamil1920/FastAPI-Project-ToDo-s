from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/admin/all")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": 'Learn the Code',
        "description": 'Need To learn everyday',
        "complete": False,
        "id": 1,
        "priority": 2,
        "owner_id": 1

    }]


def test_delete_admin(test_todo):
    response = client.delete("admin/delete_todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id).first()
    assert model is None


def test_delete_admin_not_found():
    response = client.delete("/admin/delete_todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not Found"}




