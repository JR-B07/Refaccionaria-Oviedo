# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class RolUsuario(str, Enum):
    ADMINISTRADOR = "administrador"
    GERENTE = "gerente"
    VENDEDOR = "vendedor"
    ALMACENISTA = "almacenista"
    CAJERO = "cajero"

class EstadoUsuario(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"

# Esquemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: dict

class TokenData(BaseModel):
    nombre_usuario: Optional[str] = None

class LoginRequest(BaseModel):
    nombre_usuario: str = Field(..., min_length=3, max_length=50)
    clave_acceso: str = Field(..., min_length=6, max_length=100)

# Esquemas para CRUD de usuarios
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido_paterno: Optional[str] = Field(None, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    nombre_usuario: str = Field(..., min_length=3, max_length=50)
    rol: RolUsuario = RolUsuario.VENDEDOR
    local_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    clave_acceso: str = Field(..., min_length=6, max_length=100)
    
    @validator('clave_acceso')
    def validar_fortaleza_clave(cls, v):
        if len(v) < 8:
            raise ValueError('La clave debe tener al menos 8 caracteres')
        if not any(char.isdigit() for char in v):
            raise ValueError('La clave debe contener al menos un número')
        if not any(char.isalpha() for char in v):
            raise ValueError('La clave debe contener al menos una letra')
        return v

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido_paterno: Optional[str] = Field(None, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    rol: Optional[RolUsuario] = None
    local_id: Optional[int] = None
    estado: Optional[EstadoUsuario] = None
    debe_cambiar_clave: Optional[bool] = None

class UsuarioCambioClave(BaseModel):
    clave_actual: str = Field(..., min_length=6, max_length=100)
    nueva_clave: str = Field(..., min_length=6, max_length=100)
    confirmar_clave: str = Field(..., min_length=6, max_length=100)
    
    @validator('confirmar_clave')
    def claves_coinciden(cls, v, values):
        if 'nueva_clave' in values and v != values['nueva_clave']:
            raise ValueError('Las claves nuevas no coinciden')
        return v

class UsuarioResponse(UsuarioBase):
    id: int
    estado: EstadoUsuario
    fecha_creacion: datetime
    ultimo_login: Optional[datetime]
    
    class Config:
        from_attributes = True