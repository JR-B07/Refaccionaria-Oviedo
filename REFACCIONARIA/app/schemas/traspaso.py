from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DetalleTraspasoBase(BaseModel):
    producto_id: int
    cantidad: int
    cantidad_enviada: Optional[int] = 0
    cantidad_recibida: Optional[int] = 0

class DetalleTraspasoCreate(DetalleTraspasoBase):
    pass

class DetalleTraspasoResponse(DetalleTraspasoBase):
    id: int
    traspaso_id: int
    producto_nombre: Optional[str] = None
    producto_codigo: Optional[str] = None

    class Config:
        from_attributes = True

class TraspasoBase(BaseModel):
    folio: str
    fecha: datetime
    origen_id: int
    destino_id: int
    notas: Optional[str] = None
    usuario_id: Optional[int] = None

class TraspasoCreate(TraspasoBase):
    estado: Optional[str] = "pendiente"
    detalles: Optional[List[DetalleTraspasoCreate]] = []

class TraspasoUpdate(BaseModel):
    folio: Optional[str] = None
    fecha: Optional[datetime] = None
    origen_id: Optional[int] = None
    destino_id: Optional[int] = None
    estado: Optional[str] = None
    notas: Optional[str] = None
    usuario_id: Optional[int] = None

class TraspasoResponse(TraspasoBase):
    id: int
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    # Información relacionada
    origen_nombre: Optional[str] = None
    destino_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    detalles: Optional[List[DetalleTraspasoResponse]] = []

    class Config:
        from_attributes = True
