# app/models/cliente.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase

class Cliente(ModeloBase):
    __tablename__ = "clientes"
    
    # Información básica
    alias = Column(String(100), index=True)
    nombre = Column(String(200), nullable=False, index=True)
    apellido_paterno = Column(String(100))
    apellido_materno = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    telefono = Column(String(20))
    
    # RFC y datos fiscales
    rfc = Column(String(13), unique=True, index=True)
    tipo_figura = Column(String(50), default="Persona Física")
    razon_social = Column(String(200))
    
    # Dirección
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    codigo_postal = Column(String(10))
    
    # Control
    activo = Column(Boolean, default=True)
    local_id = Column(Integer, ForeignKey("locales.id"))
    
    # Relaciones
    local = relationship("Local", back_populates="clientes")
    ventas = relationship("Venta", back_populates="cliente")
    
    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del cliente"""
        return f"{self.nombre} {self.apellido_paterno or ''} {self.apellido_materno or ''}".strip()
