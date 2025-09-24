from model.base import Base, engine
from model.academia import Academia
from model.professor import Professor
from model.aluno import Aluno

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Tabelas recriadas com sucesso.")
