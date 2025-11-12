from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

TipoMarcacao = Literal["entrada", "almoco_inicio", "almoco_fim", "saida"]

class Marcacao(BaseModel):
    colaborador_id: str = Field(..., description="Ex.: c001")
    tipo: TipoMarcacao
    timestamp: Optional[datetime] = None  # ISO 8601; se None, será 'agora'

class MarcacaoStore(Marcacao):
    id: int
