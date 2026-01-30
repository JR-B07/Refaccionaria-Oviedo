# app/models/paquete.py
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase

class Paquete(ModeloBase):
    __tablename__ = "paquetes"

    nombre = Column(String(200), nullable=False, index=True)
    descripcion = Column(Text)
    clase = Column(String(100), index=True)  # Ej: Afinación, Kit Frenos, etc.
    activo = Column(Boolean, default=True)

    # Relaciones
    items = relationship("PaqueteProducto", back_populates="paquete", cascade="all, delete-orphan")

class PaqueteProducto(ModeloBase):
    __tablename__ = "paquete_productos"

    paquete_id = Column(Integer, ForeignKey("paquetes.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    paquete = relationship("Paquete", back_populates="items")
    producto = relationship("Producto")
