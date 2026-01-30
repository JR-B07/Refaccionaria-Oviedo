# app/models/cierre_caja.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import ModeloBase

class CierreCaja(ModeloBase):
    __tablename__ = "cierres_caja"

    caja = Column(String(50), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Montos por forma de pago
    efectivo = Column(Numeric(12, 2), default=0)
    cheque = Column(Numeric(12, 2), default=0)
    tarjeta = Column(Numeric(12, 2), default=0)
    debito = Column(Numeric(12, 2), default=0)
    deposito = Column(Numeric(12, 2), default=0)
    credito = Column(Numeric(12, 2), default=0)
    vale = Column(Numeric(12, 2), default=0)
    lealtad = Column(Numeric(12, 2), default=0)
    retiros = Column(Numeric(12, 2), default=0)

    # Totales
    total_ingresos = Column(Numeric(12, 2), default=0)
    total_cierre = Column(Numeric(12, 2), default=0)

    # Referencias
    usuario = relationship("Usuario")
    local = relationship("Local")
