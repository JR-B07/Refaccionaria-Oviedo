from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.promocion import Promocion, PromocionCreate, PromocionUpdate
from app.crud import promocion as crud_promocion
from app.core.database import get_db

router = APIRouter()

@router.get("/promociones", response_model=List[Promocion])
def listar_promociones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_promocion.get_promociones(db, skip=skip, limit=limit)

@router.post("/promociones", response_model=Promocion)
def crear_promocion(promocion: PromocionCreate, db: Session = Depends(get_db)):
    return crud_promocion.create_promocion(db, promocion)

@router.put("/promociones/{promocion_id}", response_model=Promocion)
def actualizar_promocion(promocion_id: int, promocion: PromocionUpdate, db: Session = Depends(get_db)):
    db_promocion = crud_promocion.update_promocion(db, promocion_id, promocion)
    if not db_promocion:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    return db_promocion

@router.delete("/promociones/{promocion_id}")
def eliminar_promocion(promocion_id: int, db: Session = Depends(get_db)):
    ok = crud_promocion.delete_promocion(db, promocion_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    return {"ok": True}


# Endpoint para obtener solo promociones activas
@router.get("/promociones/activas", response_model=List[Promocion])
def listar_promociones_activas(db: Session = Depends(get_db)):
    return db.query(crud_promocion.Promocion).filter(crud_promocion.Promocion.activa == True).all()

# Endpoint para obtener una promoción aleatoria activa
import random
@router.get("/promociones/aleatoria", response_model=Promocion)
def promocion_aleatoria(db: Session = Depends(get_db)):
    activas = db.query(crud_promocion.Promocion).filter(crud_promocion.Promocion.activa == True).all()
    if not activas:
        raise HTTPException(status_code=404, detail="No hay promociones activas")
    return random.choice(activas)
