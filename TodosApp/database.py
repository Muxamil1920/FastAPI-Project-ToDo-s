from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# sqlite3 Database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

#PostgreSQL
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Bhat1920!@localhost/TodoApplicationDatabase'

#mysql
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Bhat1920!@127.0.0.1:3306/todoapplicationdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()