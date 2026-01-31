# app/schemas/arqueo_caja.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ArqueoCajaBase(BaseModel):
    caja: str
    local_id: int
    usuario_id: int
    turno: Optional[str] = None
    
    # Montos declarados
    efectivo_declarado: Decimal = Decimal("0")
    retiros_declarado: Decimal = Decimal("0")
    cheque_declarado: Decimal = Decimal("0")
    tarjeta_declarado: Decimal = Decimal("0")
    debito_declarado: Decimal = Decimal("0")
    deposito_declarado: Decimal = Decimal("0")
    credito_declarado: Decimal = Decimal("0")
    vale_declarado: Decimal = Decimal("0")
    lealtad_declarado: Decimal = Decimal("0")
    
    # Montos contados
    efectivo_contado: Decimal = Decimal("0")
    retiros_contado: Decimal = Decimal("0")
    cheque_contado: Decimal = Decimal("0")
    tarjeta_contado: Decimal = Decimal("0")
    debito_contado: Decimal = Decimal("0")
    deposito_contado: Decimal = Decimal("0")
    credito_contado: Decimal = Decimal("0")
    vale_contado: Decimal = Decimal("0")
    lealtad_contado: Decimal = Decimal("0")
    
    observaciones: Optional[str] = None

class ArqueoCajaCreate(ArqueoCajaBase):
    pass

class ArqueoCajaUpdate(BaseModel):
    efectivo_contado: Optional[Decimal] = None
    retiros_contado: Optional[Decimal] = None
    cheque_contado: Optional[Decimal] = None
    tarjeta_contado: Optional[Decimal] = None
    debito_contado: Optional[Decimal] = None
    deposito_contado: Optional[Decimal] = None
    credito_contado: Optional[Decimal] = None
    vale_contado: Optional[Decimal] = None
    lealtad_contado: Optional[Decimal] = None
    observaciones: Optional[str] = None
    reconciliado: Optional[bool] = None
    responsable_reconciliacion: Optional[str] = None

class ArqueoCajaOut(ArqueoCajaBase):
    id: int
    fecha_arqueo: datetime
    diferencia_efectivo: Decimal
    diferencia_retiros: Decimal
    diferencia_cheque: Decimal
    diferencia_tarjeta: Decimal
    diferencia_debito: Decimal
    diferencia_deposito: Decimal
    diferencia_credito: Decimal
    diferencia_vale: Decimal
    diferencia_lealtad: Decimal
    total_declarado: Decimal
    total_contado: Decimal
    diferencia_total: Decimal
    reconciliado: bool
    responsable_reconciliacion: Optional[str]
    
    class Config:
        from_attributes = True
