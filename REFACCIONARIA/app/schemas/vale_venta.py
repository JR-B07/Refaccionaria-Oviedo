from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ValeVentaBase(BaseModel):
    folio: str
    monto: Decimal
    concepto: Optional[str] = None
    fecha: datetime
    vendedor_id: int
    local_id: int
    descripcion: Optional[str] = None
    tipo: Optional[str] = "venta"
    venta_origen_id: Optional[int] = None

class ValeVentaCreate(ValeVentaBase):
    usado: Optional[bool] = False
    fecha_uso: Optional[datetime] = None
    destino: Optional[str] = None
    disponible: Optional[bool] = True

class ValeVentaUpdate(BaseModel):
    folio: Optional[str] = None
    monto: Optional[Decimal] = None
    concepto: Optional[str] = None
    fecha: Optional[datetime] = None
    vendedor_id: Optional[int] = None
    local_id: Optional[int] = None
    usado: Optional[bool] = None
    fecha_uso: Optional[datetime] = None
    destino: Optional[str] = None
    tipo: Optional[str] = None
    disponible: Optional[bool] = None
    descripcion: Optional[str] = None
    venta_origen_id: Optional[int] = None

class ValeVentaResponse(ValeVentaBase):
    id: int
    usado: bool
    fecha_uso: Optional[datetime] = None
    destino: Optional[str] = None
    disponible: bool
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    # Información relacionada
    vendedor_nombre: Optional[str] = None
    local_nombre: Optional[str] = None

    class Config:
        from_attributes = True
