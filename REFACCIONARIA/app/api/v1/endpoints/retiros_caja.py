# app/api/v1/endpoints/retiros_caja.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.core.database import get_db
from app.schemas.retiro_caja import RetiroCajaCreate, RetiroCajaUpdate, RetiroCajaOut
from app.models.retiro_caja import RetiroCaja
from app.models.usuario import Usuario
from app.models.local import Local
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/retiros", tags=["Retiros de Caja"])

@router.post("/caja", response_model=RetiroCajaOut)
def crear_retiro_caja(payload: RetiroCajaCreate, db: Session = Depends(get_db)):
    """Crea un nuevo retiro de caja"""
    try:
        # Verificar que el folio no exista
        existente = db.query(RetiroCaja).filter(RetiroCaja.folio == payload.folio).first()
        if existente:
            raise HTTPException(status_code=400, detail="El folio ya existe")
        
        retiro = RetiroCaja(**payload.dict())
        db.add(retiro)
        db.commit()
        db.refresh(retiro)
        return retiro
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/caja/{retiro_id}", response_model=RetiroCajaOut)
def obtener_retiro(retiro_id: int, db: Session = Depends(get_db)):
    """Obtiene un retiro por ID"""
    retiro = db.query(RetiroCaja).filter(RetiroCaja.id == retiro_id).first()
    if not retiro:
        raise HTTPException(status_code=404, detail="Retiro no encontrado")
    return retiro

@router.get("/listar")
def listar_retiros(
    local_id: int = Query(None),
    folio: str = Query(None),
    descripcion: str = Query(None),
    vendedor: str = Query(None),
    fecha_inicio: str = Query(None),
    fecha_fin: str = Query(None),
    db: Session = Depends(get_db)
):
    """Lista retiros de caja con filtros opcionales"""
    query = db.query(
        RetiroCaja.id,
        RetiroCaja.folio,
        RetiroCaja.monto,
        RetiroCaja.fecha_retiro,
        RetiroCaja.descripcion,
        RetiroCaja.local_id,
        Usuario.nombre.label('vendedor_nombre'),
        Local.nombre.label('sucursal_nombre')
    ).join(Usuario, RetiroCaja.usuario_id == Usuario.id)\
     .join(Local, RetiroCaja.local_id == Local.id)
    
    # Filtros
    if local_id:
        query = query.filter(RetiroCaja.local_id == local_id)
    
    if folio:
        query = query.filter(RetiroCaja.folio.like(f'%{folio}%'))
    
    if descripcion:
        query = query.filter(RetiroCaja.descripcion.like(f'%{descripcion}%'))
    
    if vendedor:
        query = query.filter(Usuario.nombre.like(f'%{vendedor}%'))
    
    if fecha_inicio:
        fecha_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        query = query.filter(RetiroCaja.fecha_retiro >= fecha_ini)
    
    if fecha_fin:
        fecha_f = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_f = fecha_f.replace(hour=23, minute=59, second=59)
        query = query.filter(RetiroCaja.fecha_retiro <= fecha_f)
    
    retiros = query.order_by(RetiroCaja.fecha_retiro.desc()).all()
    
    # Convertir a diccionario
    resultado = []
    for r in retiros:
        resultado.append({
            'id': r.id,
            'folio': r.folio,
            'monto': float(r.monto),
            'fecha': r.fecha_retiro.strftime('%d/%m/%Y') if r.fecha_retiro else '',
            'hora': r.fecha_retiro.strftime('%H:%M:%S') if r.fecha_retiro else '',
            'vendedor': r.vendedor_nombre,
            'sucursal': r.sucursal_nombre,
            'descripcion': r.descripcion,
            'local_id': r.local_id
        })
    
    return {
        'retiros': resultado,
        'total': len(resultado)
    }

@router.put("/caja/{retiro_id}", response_model=RetiroCajaOut)
def actualizar_retiro(
    retiro_id: int,
    payload: RetiroCajaUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un retiro de caja"""
    retiro = db.query(RetiroCaja).filter(RetiroCaja.id == retiro_id).first()
    if not retiro:
        raise HTTPException(status_code=404, detail="Retiro no encontrado")
    
    try:
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(retiro, key, value)
        
        db.commit()
        db.refresh(retiro)
        return retiro
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/caja/{retiro_id}")
def eliminar_retiro(retiro_id: int, db: Session = Depends(get_db)):
    """Elimina un retiro de caja"""
    retiro = db.query(RetiroCaja).filter(RetiroCaja.id == retiro_id).first()
    if not retiro:
        raise HTTPException(status_code=404, detail="Retiro no encontrado")
    
    try:
        db.delete(retiro)
        db.commit()
        return {"message": "Retiro eliminado exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
