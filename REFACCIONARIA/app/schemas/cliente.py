# app/schemas/cliente.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    alias: Optional[str] = None
    nombre: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    rfc: Optional[str] = None
    tipo_figura: Optional[str] = "Persona Física"
    razon_social: Optional[str] = None
    telefono: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    activo: bool = True
    local_id: Optional[int] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    rfc: Optional[str] = None
    razon_social: Optional[str] = None
    telefono: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    activo: Optional[bool] = None
    local_id: Optional[int] = None


class ClienteResponse(ClienteBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClienteOut(ClienteResponse):
    pass
