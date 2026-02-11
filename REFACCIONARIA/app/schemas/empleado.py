# app/schemas/empleado.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class EmpleadoBase(BaseModel):
    nombre: str
    puesto: str
    departamento: Optional[str] = None
    sucursal: Optional[str] = None
    organizacion: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None
    activo: bool = True
    notas: Optional[str] = None


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    puesto: Optional[str] = None
    departamento: Optional[str] = None
    sucursal: Optional[str] = None
    organizacion: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None
    activo: Optional[bool] = None
    notas: Optional[str] = None


class EmpleadoResponse(EmpleadoBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
