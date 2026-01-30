# app/models/proveedor.py
from sqlalchemy import Column, String, Numeric, Integer, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase
import enum

class TipoMoneda(enum.Enum):
    PESOS = "pesos"
    DOLARES = "dolares"

class FormaPago(enum.Enum):
    CONTADO = "contado"
    CREDITO = "credito"

class Proveedor(ModeloBase):
    __tablename__ = "proveedores"
    
    # Información General (ACCESO RAPIDO)
    clave = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    rfc = Column(String(20), index=True)
    web = Column(String(200))
    
    # Dirección
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    numero_interior = Column(String(20))
    colonia = Column(String(100))
    codigo_postal = Column(String(10))
    municipio = Column(String(100))
    estado = Column(String(100))
    ciudad = Column(String(100))
    pais = Column(String(100), default="MEXICO")
    
    # Información para Compras
    contacto_compras_nombre = Column(String(100))
    contacto_compras_email = Column(String(100))
    contacto_compras_telefono = Column(String(20))
    lista_precios_compra = Column(String(100))
    dias_entrega = Column(Integer, default=0)
    tipo_moneda = Column(Enum(TipoMoneda), default=TipoMoneda.PESOS)
    
    # Información de Descuentos
    descuento_factura = Column(Numeric(5, 2), default=0)  # Porcentaje
    descuento_listas_precio = Column(Numeric(5, 2), default=0)  # Porcentaje
    descuento_producto_factura = Column(Numeric(5, 2), default=0)  # Porcentaje
    notas_compras = Column(Text)
    
    # Información para Finanzas
    contacto_finanzas_nombre = Column(String(100))
    contacto_finanzas_email = Column(String(100))
    contacto_finanzas_telefono = Column(String(20))
    forma_pago = Column(Enum(FormaPago), default=FormaPago.CONTADO)
    dias_credito = Column(Integer, default=0)
    saldo = Column(Numeric(10, 2), default=0)
    
    # Estado
    activo = Column(String(10), default="ACTIVO")
