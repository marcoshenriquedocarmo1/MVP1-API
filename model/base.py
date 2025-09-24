# model/base.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

# Configure sua string de conexão aqui
engine = create_engine('sqlite:///database.db', echo=True)

Session = sessionmaker(bind=engine)