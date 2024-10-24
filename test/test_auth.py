from ..routers.auth import authenticate_user, get_db, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from .utils import *
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException


app.dependency_overrides[get_db] = override_get_db

def test_authenticated_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'test123', db )
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existing_user = authenticate_user('wrong_user','test123',db)
    assert non_existing_user is None

    wrong_password = authenticate_user(test_user.username, "wrong_password", db)
    assert wrong_password is None


def test_key_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires)

    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signiture':False})

    assert decode_token['sub'] == username
    assert decode_token['id'] == user_id
    assert decode_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user():
    encode = {'sub':'testuser', 'id':1, 'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)

    assert user == {'username':'testuser', 'id':1, 'role':'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Authorization Failed"