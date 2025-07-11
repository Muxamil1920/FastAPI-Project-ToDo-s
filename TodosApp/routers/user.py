from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from TodosApp.database import SessionLocal
from TodosApp.models import Users
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = "/user",
    tags=['USER']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class VerifyUser(BaseModel):
    password : str
    new_password: str = Field(min_length=6)



@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authorization Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, user_verify: VerifyUser, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verify.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Password Mismatch')
    user_model.hashed_password = bcrypt_context.hash(user_verify.new_password)
    db.add(user_model)
    db.commit()

@router.put("/update_number/{number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_number(db: db_dependency, user: user_dependency, number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authorization Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = number
    db.add(user_model)
    db.commit()






