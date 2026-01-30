from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cierre_caja import CierreCajaCreate, CierreCajaOut
from app.services.cierre_caja_service import CierreCajaService

router = APIRouter(prefix="/cajas", tags=["Cierres de Caja"])

@router.post("/cierres", response_model=CierreCajaOut)
def crear_cierre_caja(payload: CierreCajaCreate, db: Session = Depends(get_db)):
    try:
        service = CierreCajaService(db)
        return service.crear_cierre(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
