from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.core.database import get_db
from app.models.gasto import Gasto, EstadoGasto
from app.schemas.gasto import GastoCreate, GastoUpdate, GastoResponse
from app.crud.gasto import gasto as gasto_crud

router = APIRouter()


@router.get("/gastos", response_model=List[GastoResponse])
async def listar_gastos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    estado: Optional[str] = None,
    usuario: Optional[str] = None,
    departamento: Optional[str] = None,
    categoria: Optional[str] = None,
    proveedor: Optional[str] = None,
    sucursal: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos los gastos con filtros opcionales
    """
    query = db.query(Gasto)
    
    if estado:
        try:
            estado_enum = EstadoGasto[estado.upper()]
            query = query.filter(Gasto.estado == estado_enum)
        except KeyError:
            raise HTTPException(status_code=400, detail="Estado inválido")
    
    if usuario:
        query = query.filter(Gasto.usuario.ilike(f"%{usuario}%"))
    
    if departamento:
        query = query.filter(Gasto.departamento.ilike(f"%{departamento}%"))
    
    if categoria:
        query = query.filter(Gasto.categoria.ilike(f"%{categoria}%"))
    
    if proveedor:
        query = query.filter(Gasto.proveedor.ilike(f"%{proveedor}%"))
    
    if sucursal:
        query = query.filter(
            (Gasto.sucursal_origen.ilike(f"%{sucursal}%")) |
            (Gasto.sucursal_destino.ilike(f"%{sucursal}%"))
        )
    
    if fecha_inicio:
        query = query.filter(Gasto.fecha >= datetime.combine(fecha_inicio, datetime.min.time()))
    
    if fecha_fin:
        query = query.filter(Gasto.fecha <= datetime.combine(fecha_fin, datetime.max.time()))
    
    gastos = query.offset(skip).limit(limit).all()
    return gastos


@router.get("/gastos/{gasto_id}", response_model=GastoResponse)
async def obtener_gasto(
    gasto_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un gasto por ID"""
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return gasto


@router.post("/gastos", response_model=GastoResponse, status_code=201)
async def crear_gasto(
    gasto: GastoCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo gasto"""
    # Verificar si ya existe un gasto con el mismo folio
    existe = db.query(Gasto).filter(Gasto.folio == gasto.folio).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un gasto con este folio")
    
    db_gasto = Gasto(**gasto.dict())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto


@router.put("/gastos/{gasto_id}", response_model=GastoResponse)
async def actualizar_gasto(
    gasto_id: int,
    gasto: GastoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un gasto existente"""
    db_gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not db_gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = gasto.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_gasto, field, value)
    
    db.commit()
    db.refresh(db_gasto)
    return db_gasto


@router.delete("/gastos/{gasto_id}", status_code=204)
async def eliminar_gasto(
    gasto_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un gasto existente"""
    db_gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not db_gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    db.delete(db_gasto)
    db.commit()
    return None


@router.get("/gastos/estadisticas/totales")
async def obtener_totales(
    estado: Optional[str] = None,
    departamento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtiene totales de gastos por estado y departamento"""
    query = db.query(Gasto)
    
    if estado:
        try:
            estado_enum = EstadoGasto[estado.upper()]
            query = query.filter(Gasto.estado == estado_enum)
        except KeyError:
            raise HTTPException(status_code=400, detail="Estado inválido")
    
    if departamento:
        query = query.filter(Gasto.departamento == departamento)
    
    gastos = query.all()
    total = sum(g.total for g in gastos)
    
    return {
        "total_gastos": len(gastos),
        "monto_total": total,
        "promedio": total / len(gastos) if gastos else 0
    }
