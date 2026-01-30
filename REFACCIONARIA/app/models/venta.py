# app/models/venta.py
from sqlalchemy import Column, Numeric, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase
import enum

class TipoVenta(enum.Enum):
    CONTADO = "contado"
    CREDITO = "credito"
    APARTADO = "apartado"

class EstadoVenta(enum.Enum):
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    DEVUELTA = "devuelta"

class Venta(ModeloBase):
    __tablename__ = "ventas"
    
    # Información general
    folio = Column(String(50), unique=True, index=True, nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    
    # Tipo y estado
    tipo_venta = Column(Enum(TipoVenta), default=TipoVenta.CONTADO)
    estado = Column(Enum(EstadoVenta), default=EstadoVenta.COMPLETADA)
    
    # Montos
    subtotal = Column(Numeric(10, 2), default=0)
    descuento = Column(Numeric(10, 2), default=0)
    iva = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    pago_recibido = Column(Numeric(10, 2), default=0)
    cambio = Column(Numeric(10, 2), default=0)
    
    # Para crédito
    fecha_limite_pago = Column(DateTime)
    saldo_pendiente = Column(Numeric(10, 2), default=0)
    
    # Método de pago
    metodo_pago = Column(String(50))  # efectivo, tarjeta, transferencia
    
    # Relaciones
    local = relationship("Local", back_populates="ventas")
    usuario = relationship("Usuario")
    cliente = relationship("Cliente")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(ModeloBase):
    __tablename__ = "detalle_ventas"
    
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), default=0)
    importe = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_ventas")
    local = relationship("Local")