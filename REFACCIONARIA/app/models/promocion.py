from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base

class Promocion(Base):
    __tablename__ = "promociones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(120), nullable=False)
    activa = Column(Boolean, default=True)
