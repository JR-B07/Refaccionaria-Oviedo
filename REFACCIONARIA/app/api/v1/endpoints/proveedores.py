from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorResponse

router = APIRouter()

@router.get("/proveedores", response_model=List[ProveedorResponse])
async def listar_proveedores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos los proveedores"""
    proveedores = db.query(Proveedor).offset(skip).limit(limit).all()
    return proveedores

@router.get("/proveedores/{proveedor_id}", response_model=ProveedorResponse)
async def obtener_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un proveedor por ID"""
    proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.post("/proveedores", response_model=ProveedorResponse, status_code=201)
async def crear_proveedor(
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo proveedor"""
    # Verificar si ya existe un proveedor con la misma clave
    existe = db.query(Proveedor).filter(Proveedor.clave == proveedor.clave).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un proveedor con esta clave")
    
    db_proveedor = Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.put("/proveedores/{proveedor_id}", response_model=ProveedorResponse)
async def actualizar_proveedor(
    proveedor_id: int,
    proveedor: ProveedorUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un proveedor existente"""
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Verificar si la clave ya existe en otro proveedor
    if proveedor.clave and proveedor.clave != db_proveedor.clave:
        existe = db.query(Proveedor).filter(
            Proveedor.clave == proveedor.clave,
            Proveedor.id != proveedor_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe otro proveedor con esta clave")
    
    # Actualizar solo los campos proporcionados
    update_data = proveedor.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_proveedor, field, value)
    
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.delete("/proveedores/{proveedor_id}", status_code=204)
async def eliminar_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un proveedor"""
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    db.delete(db_proveedor)
    db.commit()
    return None
