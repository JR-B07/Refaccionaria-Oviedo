# app/schemas/grupo.py
from typing import Optional
from pydantic import BaseModel


class GrupoBase(BaseModel):
    nombre: str
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = True


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class GrupoOut(BaseModel):
    id: int
    nombre: str
    tipo: Optional[str]
    descripcion: Optional[str]
    activo: bool


class GrupoProductoBase(BaseModel):
    producto_id: int
    linea: Optional[str] = None
    caracteristica1: Optional[str] = None
    caracteristica2: Optional[str] = None
    clave: Optional[str] = None


class GrupoProductoCreate(GrupoProductoBase):
    pass


class GrupoProductoUpdate(BaseModel):
    linea: Optional[str] = None
    caracteristica1: Optional[str] = None
    caracteristica2: Optional[str] = None
    clave: Optional[str] = None


class GrupoProductoOut(BaseModel):
    id: int
    producto_id: int
    linea: Optional[str]
    marca: Optional[str]
    caracteristica1: Optional[str]
    caracteristica2: Optional[str]
    clave: Optional[str]
    codigo: Optional[str]
    nombre: Optional[str]


class GrupoAplicacionBase(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    motor: Optional[str] = None
    desde: Optional[int] = None
    hasta: Optional[int] = None


class GrupoAplicacionCreate(GrupoAplicacionBase):
    pass


class GrupoAplicacionUpdate(GrupoAplicacionBase):
    pass


class GrupoAplicacionOut(BaseModel):
    id: int
    marca: Optional[str]
    modelo: Optional[str]
    motor: Optional[str]
    desde: Optional[int]
    hasta: Optional[int]
