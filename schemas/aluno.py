from pydantic import BaseModel
from typing import Optional, List

class AlunoCreate(BaseModel):
    nome: str
    professor_id: int
    academia_id: int
    ativo: Optional[bool] = True

class AlunoRead(BaseModel):
    id: int
    nome: str
    professor_id: int
    academia_id: int
    data_inscricao: str
    ativo: bool

    class Config:
        orm_mode = True

# Para busca via view
class AlunoBuscaView(BaseModel):
    nome: str
    professor: str
    academia: str
    data_inscricao: str

    class Config:
        orm_mode = True

class AlunoViewSchema(BaseModel):
    id: int = 1
    nome: str = "Ana Souza"
    professor_id: int = 1
    academia_id: int = 1
    ativo: bool = True
    data_inscricao: Optional[str] = "2025-09-13T21:31:00"

class AlunoBuscaSchema(BaseModel):
    nome: str = "Ana Souza"

class AlunoDelSchema(BaseModel):
    message: str = "Aluno removido"
    id: str = "Ana Souza"

class ListagemAlunosSchema(BaseModel):
    alunos: List[AlunoViewSchema]