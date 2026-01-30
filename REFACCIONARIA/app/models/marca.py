# app/models/marca.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import ModeloBase

class Marca(ModeloBase):
    __tablename__ = "marcas"
    
    nombre = Column(String(100), unique=True, index=True, nullable=False)
    pais_origen = Column(String(100))
    activo = Column(Integer, default=1)
