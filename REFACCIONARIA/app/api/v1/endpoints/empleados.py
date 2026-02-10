# app/api/v1/endpoints/empleados.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.empleado import Empleado
from app.schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse

router = APIRouter()


@router.get("/", response_model=List[EmpleadoResponse])
async def listar_empleados(
    skip: int = 0,
    limit: int = 100,
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    puesto: Optional[str] = Query(None, description="Filtrar por puesto"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Lista todos los empleados con filtros opcionales"""
    query = db.query(Empleado)
    
    if nombre:
        query = query.filter(Empleado.nombre.ilike(f"%{nombre}%"))
    
    if puesto:
        query = query.filter(Empleado.puesto.ilike(f"%{puesto}%"))
    
    if activo is not None:
        query = query.filter(Empleado.activo == activo)
    
    empleados = query.offset(skip).limit(limit).all()
    return empleados


@router.get("/{empleado_id}", response_model=EmpleadoResponse)
async def obtener_empleado(
    empleado_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un empleado por ID"""
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.post("/", response_model=EmpleadoResponse, status_code=201)
async def crear_empleado(
    empleado: EmpleadoCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo empleado"""
    try:
        db_empleado = Empleado(**empleado.dict())
        db.add(db_empleado)
        db.commit()
        db.refresh(db_empleado)
        return db_empleado
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear empleado: {str(e)}")


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
async def actualizar_empleado(
    empleado_id: int,
    empleado: EmpleadoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un empleado existente"""
    try:
        db_empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
        if not db_empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        # Actualizar solo los campos proporcionados
        update_data = empleado.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_empleado, field, value)
        
        db.commit()
        db.refresh(db_empleado)
        return db_empleado
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar empleado: {str(e)}")


@router.delete("/{empleado_id}", status_code=204)
async def eliminar_empleado(
    empleado_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un empleado por ID"""
    try:
        db_empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
        if not db_empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        db.delete(db_empleado)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar empleado: {str(e)}")
