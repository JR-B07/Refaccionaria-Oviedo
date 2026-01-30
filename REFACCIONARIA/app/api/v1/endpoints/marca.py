# app/api/v1/endpoints/marca.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.core.database import SessionLocal
from app.models.marca import Marca
from app.models.producto import Producto
from app.schemas.marca import MarcaCreate, MarcaUpdate, MarcaOut

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/", response_model=dict)
async def listar_marcas(
    q: str = None,
    activo: int = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Listar marcas con búsqueda y filtros"""
    query = db.query(Marca)
    
    if activo is not None:
        query = query.filter(Marca.activo == activo)
    
    if q:
        query = query.filter(Marca.nombre.ilike(f"%{q}%"))
    
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    # Contar productos por marca
    items_with_count = []
    for marca in items:
        count = db.query(func.count(Producto.id)).filter(Producto.marca == marca.nombre).scalar()
        items_with_count.append({
            **{col: getattr(marca, col) for col in ['id', 'nombre', 'pais_origen', 'activo', 'fecha_creacion', 'fecha_actualizacion']},
            'productos_count': count or 0
        })
    
    return {"total": total, "items": items_with_count}

@router.get("/{marca_id}", response_model=MarcaOut)
async def obtener_marca(marca_id: int, db: Session = Depends(get_db)):
    """Obtener detalle de una marca"""
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

@router.post("/", response_model=dict)
async def crear_marca(marca: MarcaCreate, db: Session = Depends(get_db)):
    """Crear nueva marca"""
    # Verificar si ya existe
    existente = db.query(Marca).filter(Marca.nombre == marca.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="La marca ya existe")
    
    nueva_marca = Marca(**marca.dict())
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    
    return {"message": "Marca creada", "id": nueva_marca.id}

@router.put("/{marca_id}", response_model=dict)
async def actualizar_marca(marca_id: int, marca: MarcaUpdate, db: Session = Depends(get_db)):
    """Actualizar una marca"""
    db_marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    # Verificar nombre único
    if marca.nombre and marca.nombre != db_marca.nombre:
        existente = db.query(Marca).filter(Marca.nombre == marca.nombre).first()
        if existente:
            raise HTTPException(status_code=400, detail="Nombre de marca ya existe")
    
    update_data = marca.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_marca, key, value)
    
    db.commit()
    db.refresh(db_marca)
    
    return {"message": "Marca actualizada", "id": db_marca.id}

@router.delete("/{marca_id}", response_model=dict)
async def eliminar_marca(marca_id: int, db: Session = Depends(get_db)):
    """Eliminar una marca (soft delete)"""
    db_marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    # Soft delete
    db_marca.activo = 0
    db.commit()
    
    return {"message": "Marca eliminada", "id": marca_id}
