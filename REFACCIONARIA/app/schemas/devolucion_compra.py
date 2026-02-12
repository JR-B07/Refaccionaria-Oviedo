# app/schemas/devolucion_compra.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class DevolucionCompraBase(BaseModel):
    folio: str = Field(..., min_length=1, max_length=50)
    compra_id: Optional[int] = None
    factura: Optional[str] = Field(None, max_length=100)
    proveedor_id: Optional[int] = None
    estado: str = Field(default="pendiente", pattern="^(pendiente|aprobada|rechazada)$")
    fecha_devolucion: date
    nota_credito: Optional[str] = Field(None, max_length=100)
    producto_nombre: str = Field(..., min_length=1, max_length=255)
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)
    monto_total: float = Field(..., gt=0)
    descripcion: Optional[str] = None
    local_id: int
    usuario_id: int

class DevolucionCompraCreate(DevolucionCompraBase):
    pass

class DevolucionCompraUpdate(BaseModel):
    folio: Optional[str] = Field(None, min_length=1, max_length=50)
    factura: Optional[str] = Field(None, max_length=100)
    proveedor_id: Optional[int] = None
    estado: Optional[str] = Field(None, pattern="^(pendiente|aprobada|rechazada)$")
    fecha_devolucion: Optional[date] = None
    nota_credito: Optional[str] = Field(None, max_length=100)
    producto_nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    cantidad: Optional[int] = Field(None, gt=0)
    precio_unitario: Optional[float] = Field(None, gt=0)
    monto_total: Optional[float] = Field(None, gt=0)
    descripcion: Optional[str] = None

class DevolucionCompraResponse(BaseModel):
    id: int
    folio: str
    compra_id: Optional[int]
    factura: Optional[str]
    proveedor_id: Optional[int]
    proveedor_nombre: Optional[str] = None
    estado: str
    fecha_devolucion: str  # Formato YYYY-MM-DD
    nota_credito: Optional[str]
    producto_nombre: str
    cantidad: int
    precio_unitario: float
    monto_total: float
    descripcion: Optional[str]
    local_id: int
    local_nombre: Optional[str] = None
    usuario_id: int
    usuario_nombre: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
