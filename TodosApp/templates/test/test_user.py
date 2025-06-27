from .utils import *
from ..routers.user import *
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "muxamil"
    assert response.json()['email'] == "muxamil@email.com"
    assert response.json()['first_name'] == "Muzamil"
    assert response.json()['last_name'] == "Bhat"
    assert response.json()['role'] == "admin"
    assert response.json()['phone_number'] == "9682302290"

def test_change_password_success(test_user):
     response = client.put("user/change_password", json={"password":"test123","new_password":"newpassword"})
     assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid(test_user):
    response = client.put("/user/change_password", json={"password":"incorrect_password", "new_password":"testmealso"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": 'Password Mismatch'}


def test_update_number(test_user):
    response = client.put("user/update_number/12323")
    assert response.status_code == status.HTTP_204_NO_CONTENT