from ninja import Schema
from typing import Optional, List
from decimal import Decimal


# -------- TbEnderecos --------
class TbEnderecosSchemaIn(Schema):
    cep: str
    endereco: str
    cidade: str
    estado: str

class TbEnderecosSchema(Schema):
    cep: str
    endereco: str
    cidade: str
    estado: str


# -------- TbCarros --------
class TbCarrosSchema(Schema):
    id: int
    fabricante: str
    modelo: str
    especificacao: Optional[str] = None

class TbCarrosSchemaIn(Schema):
    fabricante: str
    modelo: str
    especificacao: Optional[str] = None


# -------- TbDisciplinas --------
class TbDisciplinasSchema(Schema):
    id: int
    nome_disciplina: str
    carga: int
    semestre: int


# -------- TbAlunos --------
class TbAlunosSchema(Schema):
    id: int
    nome_aluno: str
    email: Optional[str] = None
    cep: Optional[TbEnderecosSchema] = None
    carro: Optional[TbCarrosSchema] = None


class TbAlunosSchemaIn(Schema):
    nome_aluno: str
    email: Optional[str] = None
    cep: Optional[str] = None  # Chave estrangeira referenciando cep
    carro: Optional[int] = None  # ID do carro


# -------- TbNotas --------
class TbNotasSchema(Schema):
    id: int
    aluno: TbAlunosSchema
    disciplina: TbDisciplinasSchema
    nota: Optional[Decimal] = None


class TbNotasSchemaIn(Schema):
    aluno: int  # ID do aluno
    disciplina: int  # ID da disciplina
    nota: Optional[Decimal] = None

