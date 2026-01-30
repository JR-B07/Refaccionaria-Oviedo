# app/crud/arqueo_caja.py
from sqlalchemy.orm import Session
from app.models.arqueo_caja import ArqueoCaja
from app.crud.base import CRUDBase
from app.schemas.arqueo_caja import ArqueoCajaCreate, ArqueoCajaUpdate

class CRUDArqueoCaja(CRUDBase[ArqueoCaja, ArqueoCajaCreate, ArqueoCajaUpdate]):
    pass

arqueo_crud = CRUDArqueoCaja(ArqueoCaja)
