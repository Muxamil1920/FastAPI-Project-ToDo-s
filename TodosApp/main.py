from fastapi import FastAPI, status, Request
from .models import Base
from TodosApp.database import engine
from .routers import auth, todos, admin, user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    return {'status': 'Healthy'}

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="TodosApp/static"), name="static")


@app.get("/")
def test(request : Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
