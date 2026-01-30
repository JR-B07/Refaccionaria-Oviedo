# app/models/grupo.py
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase


class Grupo(ModeloBase):
    __tablename__ = "grupos"

    nombre = Column(String(200), nullable=False, index=True)
    tipo = Column(String(100), nullable=True, index=True)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    productos_rel = relationship("GrupoProducto", back_populates="grupo", cascade="all, delete-orphan")
    aplicaciones = relationship("GrupoAplicacion", back_populates="grupo", cascade="all, delete-orphan")


class GrupoProducto(ModeloBase):
    __tablename__ = "grupo_productos"

    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    # Campos adicionales para vista
    linea = Column(String(100))
    caracteristica1 = Column(String(200))
    caracteristica2 = Column(String(200))
    clave = Column(String(100))  # usualmente coincide con producto.codigo

    grupo = relationship("Grupo", back_populates="productos_rel")
    # relación simple al producto


class GrupoAplicacion(ModeloBase):
    __tablename__ = "grupo_aplicaciones"

    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    marca = Column(String(100))
    modelo = Column(String(100))
    motor = Column(String(100))
    desde = Column(Integer)
    hasta = Column(Integer)

    grupo = relationship("Grupo", back_populates="aplicaciones")
