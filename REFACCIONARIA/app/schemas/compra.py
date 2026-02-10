from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

class CompraBase(BaseModel):
    folio: str
    factura: Optional[str] = None
    fecha: date
    proveedor_id: int
    local_id: int
    total: float
    subtotal: Optional[float] = 0
    descuento: Optional[float] = 0
    iva: Optional[float] = 0
    notas: Optional[str] = None
    tipo_moneda: Optional[str] = "pesos"
    usuario_id: Optional[int] = None

class CompraCreate(CompraBase):
    estado: Optional[str] = "pendiente"

class CompraUpdate(BaseModel):
    folio: Optional[str] = None
    factura: Optional[str] = None
    fecha: Optional[date] = None
    proveedor_id: Optional[int] = None
    local_id: Optional[int] = None
    estado: Optional[str] = None
    total: Optional[float] = None
    subtotal: Optional[float] = None
    descuento: Optional[float] = None
    iva: Optional[float] = None
    notas: Optional[str] = None
    tipo_moneda: Optional[str] = None
    usuario_id: Optional[int] = None

class CompraResponse(CompraBase):
    id: int
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    # Información relacionada
    proveedor_nombre: Optional[str] = None
    local_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None

    class Config:
        from_attributes = True
