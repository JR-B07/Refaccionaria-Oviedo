# app/schemas/marca.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarcaBase(BaseModel):
    nombre: str
    pais_origen: Optional[str] = None
    activo: int = 1

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(BaseModel):
    nombre: Optional[str] = None
    pais_origen: Optional[str] = None
    activo: Optional[int] = None

class MarcaOut(MarcaBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
