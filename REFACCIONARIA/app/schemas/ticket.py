# app/schemas/ticket.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class EstatusTicket(str, Enum):
    PENDIENTE = "Pendiente"
    PARCIAL = "Parcial"
    ENTREGADO = "Entregado"

class TicketBase(BaseModel):
    folio: str = Field(..., min_length=1, max_length=50)
    partidas: int = Field(..., ge=1)
    articulo: str = Field(..., min_length=1, max_length=200)
    cliente: str = Field(..., min_length=1, max_length=150)
    fecha: datetime
    estatus: EstatusTicket = EstatusTicket.PENDIENTE

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    estatus: Optional[EstatusTicket] = None
    partidas: Optional[int] = Field(None, ge=1)
    articulo: Optional[str] = Field(None, min_length=1, max_length=200)

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TicketImpresion(BaseModel):
    folio: str = Field(..., min_length=1, max_length=50)
    exito: bool
    mensaje: str
