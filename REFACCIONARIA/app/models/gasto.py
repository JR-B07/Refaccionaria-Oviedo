from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.models.base import Base


class EstadoGasto(str, enum.Enum):
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    CANCELADO = "Cancelado"


class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String(50), unique=True, index=True, nullable=False)
    estado = Column(SQLEnum(EstadoGasto), default=EstadoGasto.PENDIENTE, nullable=False)
    fecha = Column(DateTime, default=func.now(), nullable=False)
    total = Column(Float, nullable=False)
    categoria = Column(String(100), nullable=False)
    factura = Column(String(50), nullable=True)
    usuario = Column(String(150), nullable=False)
    sucursal_origen = Column(String(100), nullable=False)
    departamento = Column(String(100), nullable=False)
    proveedor = Column(String(150), nullable=True)
    sucursal_destino = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "folio": self.folio,
            "estado": self.estado.value if isinstance(self.estado, EstadoGasto) else self.estado,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "total": self.total,
            "categoria": self.categoria,
            "factura": self.factura,
            "usuario": self.usuario,
            "sucursal_origen": self.sucursal_origen,
            "departamento": self.departamento,
            "proveedor": self.proveedor,
            "sucursal_destino": self.sucursal_destino,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
        }
