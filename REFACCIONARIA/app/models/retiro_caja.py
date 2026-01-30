# app/models/retiro_caja.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import ModeloBase

class RetiroCaja(ModeloBase):
    __tablename__ = "retiros_caja"

    folio = Column(String(50), unique=True, index=True, nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Información del retiro
    monto = Column(Numeric(12, 2), nullable=False)
    fecha_retiro = Column(DateTime, server_default=func.now())
    descripcion = Column(Text, nullable=False)
    
    # Relaciones
    local = relationship("Local", back_populates="retiros_caja")
    usuario = relationship("Usuario")
    
    def __repr__(self):
        return f"<RetiroCaja {self.folio} - ${self.monto}>"
