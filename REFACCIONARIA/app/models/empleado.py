# app/models/empleado.py
from sqlalchemy import Column, String, Integer, Boolean, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase


class Empleado(ModeloBase):
    __tablename__ = "empleados"
    
    # Información personal
    nombre = Column(String(150), nullable=False, index=True)
    puesto = Column(String(100), nullable=False, index=True)
    departamento = Column(String(100), index=True)
    sucursal = Column(String(100), index=True)
    organizacion = Column(String(150))
    
    # Fechas
    fecha_alta = Column(Date)
    fecha_baja = Column(Date)
    
    # Estado
    activo = Column(Boolean, default=True, index=True)
    
    # Información adicional
    notas = Column(Text)
    
    def __repr__(self):
        return f"<Empleado {self.id}: {self.nombre}>"
