from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from model.base import Base


class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    professor_id = Column(Integer, ForeignKey('professor.id'), nullable=True)
    academia_id = Column(Integer, ForeignKey('academia.id'))
    data_inscricao = Column(DateTime, default=datetime.now)
    ativo = Column(Boolean, default=True)

    professor = relationship('Professor', back_populates='alunos')
    academia = relationship('Academia', back_populates='alunos')