from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base

class Professor(Base):
    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True, nullable=False)  # 1 professor só pode trabalhar em 1 lugar
    academia_id = Column(Integer, ForeignKey('academia.id'))
    data_insercao = Column(DateTime, default=datetime.now)
    ativo = Column(Boolean, default=True)

    academia = relationship('Academia', back_populates='professores')
    alunos = relationship('Aluno', back_populates='professor')
