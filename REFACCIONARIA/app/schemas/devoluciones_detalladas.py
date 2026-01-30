from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DevolucionDetalleResponse(BaseModel):
    fecha_venta: str
    fecha_devolucion: str
    sucursal: str
    vendedor: str
    folio: str
    producto: str
    monto: str
    cliente: str
    estado: str
    total: float

    class Config:
        from_attributes = True

class DevolucionesDetalladasResponse(BaseModel):
    total: int
    devoluciones: List[DevolucionDetalleResponse]
    total_monto: float
