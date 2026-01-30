# app/schemas/paquete.py
from typing import List, Optional
from pydantic import BaseModel

class PaqueteBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    clase: Optional[str] = None
    activo: Optional[bool] = True

class PaqueteCreate(PaqueteBase):
    pass

class PaqueteUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    clase: Optional[str] = None
    activo: Optional[bool] = None

class PaqueteItemBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class PaqueteItemCreate(PaqueteItemBase):
    pass

class PaqueteItemUpdate(BaseModel):
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None

class PaqueteOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    clase: Optional[str]
    activo: bool
    total_items: int
    precio_total: float

class PaqueteItemOut(BaseModel):
    id: int
    producto_id: int
    codigo: str
    nombre: str
    cantidad: int
    precio_unitario: float
    total: float

class PaqueteDetalleOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    clase: Optional[str]
    activo: bool
    precio_total: float
    items: List[PaqueteItemOut]
