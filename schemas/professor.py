from pydantic import BaseModel
from typing import Optional, List

class ProfessorCreate(BaseModel):
    nome: str
    academia_id: int
    ativo: Optional[bool] = True

class ProfessorRead(BaseModel):
    id: int
    nome: str
    academia_id: int
    data_insercao: str
    ativo: bool

    class Config:
        orm_mode = True

class ProfessorViewSchema(BaseModel):
    id: int = 1
    nome: str = "Carlos Andrade"
    academia_id: int = 1
    ativo: bool = True
    data_insercao: Optional[str] = "2025-09-13T21:31:00"

class ProfessorBuscaSchema(BaseModel):
    nome: str = "Carlos Andrade"

class ProfessorDelSchema(BaseModel):
    message: str = "Professor removido"
    id: str = "Carlos Andrade"

class ListagemProfessoresSchema(BaseModel):
    professores: List[ProfessorViewSchema]