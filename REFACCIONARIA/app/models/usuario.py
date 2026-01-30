# app/models/usuario.py
from sqlalchemy import Column, String, Integer, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import ModeloBase

class RolUsuario(enum.Enum):
    ADMINISTRADOR = "administrador"
    GERENTE = "gerente"
    VENDEDOR = "vendedor"
    ALMACENISTA = "almacenista"
    CAJERO = "cajero"

class EstadoUsuario(enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"

class Usuario(ModeloBase):
    __tablename__ = "usuarios"
    
    # Información personal
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100))
    apellido_materno = Column(String(100))
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(20))
    
    # Autenticación
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    clave_hash = Column(String(255), nullable=False)
    
    # Roles y permisos
    rol = Column(Enum(RolUsuario), default=RolUsuario.VENDEDOR)
    estado = Column(Enum(EstadoUsuario), default=EstadoUsuario.ACTIVO)
    
    # Local asignado
    local_id = Column(Integer, ForeignKey("locales.id"))
    
    # Auditoría
    ultimo_login = Column(DateTime(timezone=True))
    intentos_fallidos = Column(Integer, default=0)
    bloqueado_hasta = Column(DateTime(timezone=True))
    
    # Configuración
    debe_cambiar_clave = Column(Boolean, default=True)
    tema_interfaz = Column(String(20), default="claro")  # claro/oscuro
    
    # Relaciones
    local = relationship("Local", back_populates="usuarios")
    ventas = relationship("Venta", back_populates="usuario")
    
    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido_paterno or ''} {self.apellido_materno or ''}".strip()
    
    def verificar_clave(self, clave_plana: str) -> bool:
        """Verifica si la clave en texto plano coincide con el hash"""
        from app.core.security import verify_password
        return verify_password(clave_plana, self.clave_hash)