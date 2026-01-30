# app/api/v1/endpoints/locales.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.local import Local

router = APIRouter()

@router.get("/")
async def listar_locales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar locales/sucursales
    """
    locales = db.query(Local).offset(skip).limit(limit).all()
    return [
        {
            "id": local.id,
            "nombre": local.nombre,
            "direccion": local.direccion,
            "telefono": local.telefono,
            "email": local.email
        }
        for local in locales
    ]

# Alias para compatibilidad: /locales/listar
@router.get("/listar")
async def listar_locales_alias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return await listar_locales(skip=skip, limit=limit, db=db)

@router.get("/{local_id}")
async def obtener_local(
    local_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener local por ID
    """
    local = db.query(Local).filter(Local.id == local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    return {
        "id": local.id,
        "nombre": local.nombre,
        "direccion": local.direccion,
        "telefono": local.telefono,
        "email": local.email
    }
