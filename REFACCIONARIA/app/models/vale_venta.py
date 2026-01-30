# app/models/vale_venta.py
from sqlalchemy import Column, String, Numeric, Integer, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase
import enum

class TipoVale(enum.Enum):
    VENTA = "venta"
    DEVOLUCION = "devolucion"

class EstadoVale(enum.Enum):
    DISPONIBLE = "disponible"
    USADO = "usado"
    CANCELADO = "cancelado"

class ValeVenta(ModeloBase):
    __tablename__ = "vales_venta"
    
    # Información básica
    folio = Column(String(50), unique=True, index=True, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    concepto = Column(String(200))
    fecha = Column(DateTime, nullable=False)
    
    # Relaciones
    vendedor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    
    # Estado y uso
    usado = Column(Boolean, default=False)
    fecha_uso = Column(DateTime)  # Fecha en que se usó el vale
    destino = Column(String(50))  # Folio de venta donde se usó
    tipo = Column(Enum(TipoVale), default=TipoVale.VENTA)
    disponible = Column(Boolean, default=True)
    
    # Información adicional
    descripcion = Column(String(500))
    venta_origen_id = Column(Integer, ForeignKey("ventas.id"))  # Venta que generó el vale
    
    # Relaciones
    vendedor = relationship("Usuario")
    local = relationship("Local")
    venta_origen = relationship("Venta", foreign_keys=[venta_origen_id])
