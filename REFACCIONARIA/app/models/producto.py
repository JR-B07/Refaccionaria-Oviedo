# app/models/producto.py
from sqlalchemy import Column, String, Numeric, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase

class Producto(ModeloBase):
    __tablename__ = "productos"
    
    # Información básica
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    codigo_barras = Column(String(100), unique=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    marca = Column(String(100))
    modelo = Column(String(100))
    categoria = Column(String(100))
    
    # Precios
    precio_compra = Column(Numeric(10, 2), nullable=False)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    precio_venta_credito = Column(Numeric(10, 2))
    
    # Control de inventario
    stock_total = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    
    # Ubicación física
    ubicacion_estante = Column(String(50))
    ubicacion_fila = Column(String(10))
    ubicacion_columna = Column(String(10))
    
    # Para auto partes específicas
    compatibilidad = Column(JSON)  # Ej: {"marcas": ["Toyota", "Honda"], "modelos": ["Corolla", "Civic"]}
    año_inicio = Column(Integer)
    año_fin = Column(Integer)
    
    # Relaciones
    inventario_locales = relationship("InventarioLocal", back_populates="producto")
    detalle_ventas = relationship("DetalleVenta", back_populates="producto")

class InventarioLocal(ModeloBase):
    __tablename__ = "inventario_local"
    
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    stock = Column(Integer, default=0)
    stock_reservado = Column(Integer, default=0)  # Para ventas en proceso
    
    # Relaciones
    producto = relationship("Producto", back_populates="inventario_locales")
    local = relationship("Local", back_populates="productos_inventario")