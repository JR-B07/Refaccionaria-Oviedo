from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cierre_caja import CierreCajaCreate, CierreCajaOut
from app.services.cierre_caja_service import CierreCajaService
from typing import List, Optional
from datetime import date

router = APIRouter(prefix="/cajas", tags=["Cierres de Caja"])

@router.get("/cierres", response_model=List[CierreCajaOut])
def listar_cierres_caja(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicial"),
    fecha_fin: Optional[date] = Query(None, description="Fecha final"),
    caja: Optional[str] = Query(None, description="Nombre de caja"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """Lista todos los cierres de caja con filtros opcionales"""
    try:
        service = CierreCajaService(db)
        return service.listar_cierres(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            caja=caja,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cierres", response_model=CierreCajaOut)
def crear_cierre_caja(payload: CierreCajaCreate, db: Session = Depends(get_db)):
    try:
        service = CierreCajaService(db)
        return service.crear_cierre(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
