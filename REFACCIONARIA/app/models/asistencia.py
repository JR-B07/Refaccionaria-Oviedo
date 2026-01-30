# app/models/asistencia.py
from sqlalchemy import Column, String, Date, Time, UniqueConstraint
from app.models.base import ModeloBase

class AsistenciaEmpleado(ModeloBase):
    __tablename__ = "asistencia_empleados"
    __table_args__ = (
        UniqueConstraint('nombre', 'fecha', name='uq_asistencia_nombre_fecha'),
    )

    nombre = Column(String(150), nullable=False, index=True)
    sucursal = Column(String(100), nullable=True)
    fecha = Column(Date, nullable=False, index=True)

    entrada = Column(Time, nullable=True)
    comida = Column(Time, nullable=True)
    regreso = Column(Time, nullable=True)
    salida = Column(Time, nullable=True)
