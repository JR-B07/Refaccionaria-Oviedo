# app/schemas/venta.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    descuento: float = 0
    importe: float

class DetalleVentaResponse(BaseModel):
    id: int
    venta_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    descuento: float
    importe: float

    class Config:
        from_attributes = True

class VentaCreate(BaseModel):
    folio: str
    local_id: int
    usuario_id: int
    cliente_id: Optional[int] = None
    estado: str = "completada"
    tipo_venta: str = "contado"
    subtotal: float = 0
    descuento: float = 0
    iva: float = 0
    total: float
    pago_recibido: float = 0
    cambio: float = 0
    metodo_pago: str = "efectivo"
    fecha_limite_pago: Optional[datetime] = None
    saldo_pendiente: float = 0
    detalles: Optional[List[DetalleVentaCreate]] = None

class VentaResponse(BaseModel):
    id: int
    folio: str
    local_id: int
    usuario_id: int
    cliente_id: Optional[int]
    tipo_venta: str
    estado: str
    subtotal: float
    descuento: float
    iva: float
    total: float
    pago_recibido: float
    cambio: float
    metodo_pago: str
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    detalles: List[DetalleVentaResponse] = []

    class Config:
        from_attributes = True
