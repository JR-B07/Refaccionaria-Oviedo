# app/models/devolucion_compra.py
from sqlalchemy import Column, String, Numeric, Integer, Enum, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase
import enum

class EstadoDevolucionCompra(enum.Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"

class DevolucionCompra(ModeloBase):
    __tablename__ = "devoluciones_compra"
    
    # Información básica
    folio = Column(String(50), unique=True, index=True, nullable=False)
    compra_id = Column(Integer, ForeignKey("compras.id"))
    factura = Column(String(100), index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    estado = Column(Enum(EstadoDevolucionCompra, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=EstadoDevolucionCompra.PENDIENTE.value)
    fecha_devolucion = Column(Date, nullable=False)
    nota_credito = Column(String(100))
    
    # Detalles del producto devuelto
    producto_nombre = Column(String(255), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    monto_total = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text)
    
    # Relaciones
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relationships
    compra = relationship("Compra", foreign_keys=[compra_id])
    proveedor = relationship("Proveedor")
    local = relationship("Local")
    usuario = relationship("Usuario")
