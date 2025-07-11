from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from TodosApp.database import SessionLocal
from TodosApp.models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from fastapi.templating import Jinja2Templates

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token : str
    token_type : str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY ="49077fed236851aafed8d347f5bbe6dd0e348c4dfb2d46276cba3d51ab6a0d43"
ALGORITHM = "HS256"

db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

templates = Jinja2Templates(directory="TodosApp/templates")

### Pages ###

@router.get("/login-page")
def render_login_page(request : Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request : Request):
    return templates.TemplateResponse("register.html", {"request": request})


### Api Routes ###
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id':user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization Failed')
        return {'username': username, 'id': user_id, 'role':role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization Failed')



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        phone_number = create_user_request.phone_number,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_token(form_data: auth_dependency, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization Failed')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'Bearer'}


