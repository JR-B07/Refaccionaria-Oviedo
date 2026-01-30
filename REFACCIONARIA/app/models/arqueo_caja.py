# app/models/arqueo_caja.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import ModeloBase

class ArqueoCaja(ModeloBase):
    __tablename__ = "arqueos_caja"

    caja = Column(String(50), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Información del arqueo
    fecha_arqueo = Column(DateTime, server_default=func.now())
    turno = Column(String(50), nullable=True)  # Mañana, Tarde, Noche
    
    # Montos declarados
    efectivo_declarado = Column(Numeric(12, 2), default=0)
    retiros_declarado = Column(Numeric(12, 2), default=0)
    cheque_declarado = Column(Numeric(12, 2), default=0)
    tarjeta_declarado = Column(Numeric(12, 2), default=0)
    debito_declarado = Column(Numeric(12, 2), default=0)
    deposito_declarado = Column(Numeric(12, 2), default=0)
    credito_declarado = Column(Numeric(12, 2), default=0)
    vale_declarado = Column(Numeric(12, 2), default=0)
    lealtad_declarado = Column(Numeric(12, 2), default=0)
    
    # Montos contados (físicamente verificados)
    efectivo_contado = Column(Numeric(12, 2), default=0)
    retiros_contado = Column(Numeric(12, 2), default=0)
    cheque_contado = Column(Numeric(12, 2), default=0)
    tarjeta_contado = Column(Numeric(12, 2), default=0)
    debito_contado = Column(Numeric(12, 2), default=0)
    deposito_contado = Column(Numeric(12, 2), default=0)
    credito_contado = Column(Numeric(12, 2), default=0)
    vale_contado = Column(Numeric(12, 2), default=0)
    lealtad_contado = Column(Numeric(12, 2), default=0)
    
    # Diferencias
    diferencia_efectivo = Column(Numeric(12, 2), default=0)
    diferencia_retiros = Column(Numeric(12, 2), default=0)
    diferencia_cheque = Column(Numeric(12, 2), default=0)
    diferencia_tarjeta = Column(Numeric(12, 2), default=0)
    diferencia_debito = Column(Numeric(12, 2), default=0)
    diferencia_deposito = Column(Numeric(12, 2), default=0)
    diferencia_credito = Column(Numeric(12, 2), default=0)
    diferencia_vale = Column(Numeric(12, 2), default=0)
    diferencia_lealtad = Column(Numeric(12, 2), default=0)
    
    # Totales
    total_declarado = Column(Numeric(12, 2), default=0)
    total_contado = Column(Numeric(12, 2), default=0)
    diferencia_total = Column(Numeric(12, 2), default=0)
    
    # Detalles
    observaciones = Column(Text, nullable=True)
    reconciliado = Column(Boolean, default=False)
    responsable_reconciliacion = Column(String(255), nullable=True)
    
    # Referencias
    usuario = relationship("Usuario")
    local = relationship("Local")
