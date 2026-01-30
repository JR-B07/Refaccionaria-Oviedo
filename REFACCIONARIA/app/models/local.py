# app/models/local.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase

class Local(ModeloBase):
    __tablename__ = "locales"
    
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    email = Column(String(100))
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="local")
    clientes = relationship("Cliente", back_populates="local")
    ventas = relationship("Venta", back_populates="local")
    productos_inventario = relationship("InventarioLocal", back_populates="local")
    retiros_caja = relationship("RetiroCaja", back_populates="local")
