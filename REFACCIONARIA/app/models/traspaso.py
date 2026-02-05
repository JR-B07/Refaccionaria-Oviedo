# app/models/traspaso.py
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase
import enum

class EstadoTraspaso(enum.Enum):
    PENDIENTE = "pendiente"
    EN_TRANSITO = "transito"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class Traspaso(ModeloBase):
    __tablename__ = "traspasos"
    
    # Información básica
    folio = Column(String(50), unique=True, index=True, nullable=False)
    estado = Column(Enum(EstadoTraspaso, length=20), default=EstadoTraspaso.PENDIENTE)
    fecha = Column(DateTime, nullable=False)
    
    # Origen y destino
    origen_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    destino_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    
    # Información adicional
    notas = Column(Text)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))  # Usuario que creó el traspaso
    
    # Relaciones
    origen = relationship("Local", foreign_keys=[origen_id])
    destino = relationship("Local", foreign_keys=[destino_id])
    usuario = relationship("Usuario")
    detalles = relationship("DetalleTraspaso", back_populates="traspaso", cascade="all, delete-orphan")

class DetalleTraspaso(ModeloBase):
    __tablename__ = "detalle_traspasos"
    
    traspaso_id = Column(Integer, ForeignKey("traspasos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    cantidad_enviada = Column(Integer, default=0)  # Cantidad realmente enviada
    cantidad_recibida = Column(Integer, default=0)  # Cantidad recibida en destino
    
    # Relaciones
    traspaso = relationship("Traspaso", back_populates="detalles")
    producto = relationship("Producto")
