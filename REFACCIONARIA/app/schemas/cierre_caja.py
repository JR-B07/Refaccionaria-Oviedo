# app/schemas/cierre_caja.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CierreCajaResponse(BaseModel):
    caja: str
    vendedor: str
    apertura: str
    hora_apertura: str
    cierre: str
    hora_cierre: str
    total_cierre: float
    
    class Config:
        from_attributes = True

class CierreCajaListResponse(BaseModel):
    total: int
    cierres: list[CierreCajaResponse]


class CierreCajaCreate(BaseModel):
    caja: str
    local_id: int
    usuario_id: int
    efectivo: float = 0
    cheque: float = 0
    tarjeta: float = 0
    debito: float = 0
    deposito: float = 0
    credito: float = 0
    vale: float = 0
    lealtad: float = 0
    retiros: float = 0


class CierreCajaOut(BaseModel):
    id: int
    caja: str
    local_id: int
    usuario_id: int
    efectivo: float
    cheque: float
    tarjeta: float
    debito: float
    deposito: float
    credito: float
    vale: float
    lealtad: float
    retiros: float
    total_ingresos: float
    total_cierre: float
    
    class Config:
        from_attributes = True
