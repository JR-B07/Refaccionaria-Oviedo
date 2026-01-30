from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class CompraBase(BaseModel):
    folio: str
    factura: Optional[str] = None
    fecha: datetime
    proveedor_id: int
    local_id: int
    total: Decimal
    subtotal: Optional[Decimal] = 0
    descuento: Optional[Decimal] = 0
    iva: Optional[Decimal] = 0
    notas: Optional[str] = None
    tipo_moneda: Optional[str] = "pesos"
    usuario_id: Optional[int] = None

class CompraCreate(CompraBase):
    estado: Optional[str] = "pendiente"

class CompraUpdate(BaseModel):
    folio: Optional[str] = None
    factura: Optional[str] = None
    fecha: Optional[datetime] = None
    proveedor_id: Optional[int] = None
    local_id: Optional[int] = None
    estado: Optional[str] = None
    total: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None
    descuento: Optional[Decimal] = None
    iva: Optional[Decimal] = None
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
