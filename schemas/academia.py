from pydantic import BaseModel
from typing import Optional

class AcademiaCreate(BaseModel):
    nome: str
    responsavel: str

class AcademiaRead(BaseModel):
    id: int
    nome: str
    responsavel: str
    data_insercao: str

    class Config:
        orm_mode = True

class AcademiaViewSchema(BaseModel):
    """Define como uma academia será retornada: dados básicos da academia."""
    id: int = 1
    nome: str = "Academia High Class"
    responsavel: str = "Bruce Wayne"
    data_insercao: Optional[str] = "2025-09-13T21:31:00"

class AcademiaBuscaSchema(BaseModel):
    nome: str    