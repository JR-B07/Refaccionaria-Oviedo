# app/models/compra.py
from sqlalchemy import Column, String, Numeric, Integer, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase
import enum

class EstadoCompra(enum.Enum):
    PENDIENTE = "pendiente"
    COMPLETO = "completo"
    CANCELADO = "cancelado"
    PARCIAL = "parcial"

class Compra(ModeloBase):
    __tablename__ = "compras"
    
    # Información básica
    folio = Column(String(50), unique=True, index=True, nullable=False)
    factura = Column(String(100), index=True)  # Número de factura del proveedor
    estado = Column(Enum(EstadoCompra), default=EstadoCompra.PENDIENTE)
    fecha = Column(DateTime, nullable=False)
    
    # Relaciones
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))  # Usuario que registró la compra
    
    # Montos
    subtotal = Column(Numeric(10, 2), default=0)
    descuento = Column(Numeric(10, 2), default=0)
    iva = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    
    # Información adicional
    notas = Column(Text)
    tipo_moneda = Column(String(20), default="pesos")  # pesos, dolares
    
    # Relaciones
    proveedor = relationship("Proveedor")
    local = relationship("Local")
    usuario = relationship("Usuario")
    detalles = relationship("DetalleCompra", back_populates="compra", cascade="all, delete-orphan")

class DetalleCompra(ModeloBase):
    __tablename__ = "detalle_compras"
    
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), default=0)
    importe = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto")
