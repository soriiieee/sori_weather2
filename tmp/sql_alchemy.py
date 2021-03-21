from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
# reference -> https://qiita.com/tomo0/items/a762b1bc0f192a55eae8

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime

# DATABASE setting ....
user_name = "sori"
password = "password"
host_ip = "reiwa"
db_name = "weather"
DATABASE = f'mysql://{user_name}:{password}@{host_ip}/{db_name}?charset=utf8'

# ENGINE setting ....
ENGINE = create_engine(
  DATABASE,
  encoding = "utf-8",
  echo =True
)

# Session setting ....
session = scoped_session(
  sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = ENGINE,
  )
)

Base = declarative_base()
Base.query = session.query_property()
print(Base)
print(Base.query)
