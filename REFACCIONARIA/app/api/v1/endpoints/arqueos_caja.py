# app/api/v1/endpoints/arqueos_caja.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.arqueo_caja import ArqueoCajaCreate, ArqueoCajaUpdate, ArqueoCajaOut
from app.services.arqueo_caja_service import ArqueoCajaService

router = APIRouter(prefix="/arqueos", tags=["Arqueos de Caja"])

@router.post("/caja", response_model=ArqueoCajaOut)
def crear_arqueo_caja(payload: ArqueoCajaCreate, db: Session = Depends(get_db)):
    """Crea un nuevo arqueo de caja"""
    try:
        service = ArqueoCajaService(db)
        return service.crear_arqueo(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/caja/{arqueo_id}", response_model=ArqueoCajaOut)
def obtener_arqueo(arqueo_id: int, db: Session = Depends(get_db)):
    """Obtiene un arqueo por ID"""
    service = ArqueoCajaService(db)
    arqueo = service.obtener_arqueo(arqueo_id)
    if not arqueo:
        raise HTTPException(status_code=404, detail="Arqueo no encontrado")
    return arqueo

@router.get("/listar", response_model=list[ArqueoCajaOut])
def listar_arqueos(
    caja: str = Query(None),
    local_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """Lista arqueos de caja con filtros opcionales"""
    service = ArqueoCajaService(db)
    return service.listar_arqueos(caja=caja, local_id=local_id)

@router.put("/caja/{arqueo_id}", response_model=ArqueoCajaOut)
def actualizar_arqueo(
    arqueo_id: int,
    payload: ArqueoCajaUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un arqueo de caja"""
    try:
        service = ArqueoCajaService(db)
        return service.actualizar_arqueo(arqueo_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/caja/{arqueo_id}")
def eliminar_arqueo(arqueo_id: int, db: Session = Depends(get_db)):
    """Elimina un arqueo de caja"""
    try:
        service = ArqueoCajaService(db)
        service.eliminar_arqueo(arqueo_id)
        return {"message": "Arqueo eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
