from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base


class Academia(Base):
    __tablename__ = 'academia'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True, nullable=False)
    responsavel = Column(String(140), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    professores = relationship('Professor', back_populates='academia')
    alunos = relationship('Aluno', back_populates='academia')