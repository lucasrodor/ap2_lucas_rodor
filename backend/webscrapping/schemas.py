from ninja import Schema
from typing import Optional
from datetime import datetime

class ImovelIn(Schema):
    titulo: str
    preco: Optional[float] = None
    endereco: Optional[str] = None
    detalhes: Optional[str] = None
    descricao: Optional[str] = None
    link: str
    tamanho: Optional[str] = None
    quartos: Optional[str] = None
    vagas: Optional[str] = None
    suites: Optional[str] = None
    plantas: Optional[str] = None

class ImovelOut(ImovelIn):
    id: int
    data_extracao: datetime
