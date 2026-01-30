from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoGastoSchema(str, Enum):
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    CANCELADO = "Cancelado"


class GastoBase(BaseModel):
    folio: str
    estado: EstadoGastoSchema = EstadoGastoSchema.PENDIENTE
    fecha: Optional[datetime] = None
    total: float
    categoria: str
    factura: Optional[str] = None
    usuario: str
    sucursal_origen: str
    departamento: str
    proveedor: Optional[str] = None
    sucursal_destino: Optional[str] = None
    descripcion: Optional[str] = None


class GastoCreate(GastoBase):
    pass


class GastoUpdate(BaseModel):
    estado: Optional[EstadoGastoSchema] = None
    fecha: Optional[datetime] = None
    total: Optional[float] = None
    categoria: Optional[str] = None
    factura: Optional[str] = None
    usuario: Optional[str] = None
    sucursal_origen: Optional[str] = None
    departamento: Optional[str] = None
    proveedor: Optional[str] = None
    sucursal_destino: Optional[str] = None
    descripcion: Optional[str] = None


class GastoResponse(GastoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
