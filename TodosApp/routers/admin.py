from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status
from TodosApp.models import Todos
from TodosApp.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['ADMIN']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") not in ["admin","Admin"]:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    return db.query(Todos).all()

@router.delete("/delete_todo/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user:user_dependency, db:db_dependency, user_id:int =Path(gt=0)):
    if user is None or user.get("role") not in ["admin","Admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    db_model = db.query(Todos).filter(Todos.id == user_id).first()
    if db_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not Found")
    db.delete(db_model)
    db.commit()
