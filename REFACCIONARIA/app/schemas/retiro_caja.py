# app/schemas/retiro_caja.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class RetiroCajaBase(BaseModel):
    folio: str
    local_id: int
    usuario_id: int
    monto: Decimal
    descripcion: str

class RetiroCajaCreate(RetiroCajaBase):
    pass

class RetiroCajaUpdate(BaseModel):
    monto: Optional[Decimal] = None
    descripcion: Optional[str] = None

class RetiroCajaOut(RetiroCajaBase):
    id: int
    fecha_retiro: datetime
    
    class Config:
        from_attributes = True
