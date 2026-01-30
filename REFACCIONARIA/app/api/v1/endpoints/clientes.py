# app/api/v1/endpoints/clientes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, and_

from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse, ClienteOut
from app.models.cliente import Cliente
from app.core.database import get_db

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteOut)
async def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crear nuevo cliente"""
    try:
        # Verificar si ya existe un cliente con el mismo RFC
        if cliente.rfc:
            cliente_existente = db.query(Cliente).filter(Cliente.rfc == cliente.rfc).first()
            if cliente_existente:
                raise HTTPException(status_code=400, detail="Ya existe un cliente con ese RFC")
        
        # Verificar si ya existe un cliente con el mismo email
        if cliente.email:
            cliente_existente = db.query(Cliente).filter(Cliente.email == cliente.email).first()
            if cliente_existente:
                raise HTTPException(status_code=400, detail="Ya existe un cliente con ese email")
        
        nuevo_cliente = Cliente(**cliente.dict())
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ClienteOut])
async def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar todos los clientes"""
    query = db.query(Cliente)
    
    if activo is not None:
        query = query.filter(Cliente.activo == activo)
    
    clientes = query.order_by(desc(Cliente.id)).offset(skip).limit(limit).all()
    return clientes


@router.get("/{cliente_id}", response_model=ClienteOut)
async def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener cliente por ID"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteOut)
async def actualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar cliente"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    try:
        # Verificar RFC único
        if cliente_update.rfc and cliente_update.rfc != cliente.rfc:
            cliente_existente = db.query(Cliente).filter(
                and_(Cliente.rfc == cliente_update.rfc, Cliente.id != cliente_id)
            ).first()
            if cliente_existente:
                raise HTTPException(status_code=400, detail="Ya existe un cliente con ese RFC")
        
        # Verificar email único
        if cliente_update.email and cliente_update.email != cliente.email:
            cliente_existente = db.query(Cliente).filter(
                and_(Cliente.email == cliente_update.email, Cliente.id != cliente_id)
            ).first()
            if cliente_existente:
                raise HTTPException(status_code=400, detail="Ya existe un cliente con ese email")
        
        # Actualizar solo los campos que vienen en la request
        actualizar_datos = cliente_update.dict(exclude_unset=True)
        for campo, valor in actualizar_datos.items():
            setattr(cliente, campo, valor)
        
        db.commit()
        db.refresh(cliente)
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{cliente_id}", response_model=ClienteOut)
async def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Eliminar cliente marcándolo como inactivo (soft delete)"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    try:
        cliente.activo = False
        db.commit()
        db.refresh(cliente)
        return cliente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/buscar/nombre", response_model=List[ClienteOut])
async def buscar_cliente_por_nombre(
    nombre: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Buscar cliente por nombre"""
    clientes = db.query(Cliente).filter(
        or_(
            Cliente.nombre.ilike(f"%{nombre}%"),
            Cliente.apellido_paterno.ilike(f"%{nombre}%"),
            Cliente.apellido_materno.ilike(f"%{nombre}%"),
            Cliente.rfc.ilike(f"%{nombre}%"),
            Cliente.email.ilike(f"%{nombre}%")
        )
    ).all()
    return clientes