from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..models import Todos


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'muxamil','id': 1, 'role': 'admin'}

@pytest.fixture()
def test_todo():
    db = TestingSessionLocal()
    user = {'username':'muxamil','id': 1, 'role': 'admin'}
    todo = Todos(
        title = 'Learn the Code',
        description = 'Need To learn everyday',
        complete = False,
        priority = 2,
        owner_id = user['id']
    )
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM Todos;'))
        connection.commit()

client = TestClient(app)