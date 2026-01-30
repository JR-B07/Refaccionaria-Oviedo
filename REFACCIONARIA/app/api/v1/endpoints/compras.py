from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import get_current_user
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.compra import Compra, EstadoCompra
from app.models.proveedor import Proveedor
from app.models.local import Local
from app.models.usuario import Usuario
from app.schemas.compra import CompraResponse, CompraCreate

router = APIRouter()

@router.get("/compras", response_model=List[CompraResponse])
async def listar_compras(
    folio: Optional[str] = Query(None, description="Folio de la compra"),
    factura: Optional[str] = Query(None, description="Número de factura"),
    proveedor_id: Optional[int] = Query(None, description="ID del proveedor"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD"),
    estado: Optional[str] = Query(None, description="Estado de la compra"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista compras SOLO de la sucursal del usuario autenticado, con filtros opcionales
    """
    local_id = current_user["local_id"]
    query = db.query(Compra).filter(Compra.local_id == local_id)

    # Aplicar filtros
    if folio:
        query = query.filter(Compra.folio.ilike(f"%{folio}%"))
    if factura:
        query = query.filter(Compra.factura.ilike(f"%{factura}%"))
    if proveedor_id:
        query = query.filter(Compra.proveedor_id == proveedor_id)
    if estado:
        query = query.filter(Compra.estado == estado)
    if fecha_inicio:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        query = query.filter(Compra.fecha >= fecha_inicio_dt)
    if fecha_fin:
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        query = query.filter(Compra.fecha <= fecha_fin_dt)

    # Ordenar por fecha descendente
    query = query.order_by(Compra.fecha.desc())

    # Ejecutar query
    compras_db = query.offset(skip).limit(limit).all()
    
    # Formatear respuesta
    compras = []
    for compra in compras_db:
        proveedor = db.query(Proveedor).filter(Proveedor.id == compra.proveedor_id).first()
        local = db.query(Local).filter(Local.id == compra.local_id).first()
        usuario = db.query(Usuario).filter(Usuario.id == compra.usuario_id).first() if compra.usuario_id else None
        
        compra_dict = {
            "id": compra.id,
            "folio": compra.folio,
            "factura": compra.factura,
            "fecha": compra.fecha,
            "proveedor_id": compra.proveedor_id,
            "local_id": compra.local_id,
            "estado": compra.estado.value if compra.estado else "pendiente",
            "total": compra.total,
            "subtotal": compra.subtotal,
            "descuento": compra.descuento,
            "iva": compra.iva,
            "notas": compra.notas,
            "tipo_moneda": compra.tipo_moneda,
            "usuario_id": compra.usuario_id,
            "fecha_creacion": compra.fecha_creacion,
            "fecha_actualizacion": compra.fecha_actualizacion,
            "proveedor_nombre": proveedor.nombre if proveedor else None,
            "local_nombre": local.nombre if local else None,
            "usuario_nombre": usuario.nombre_completo if usuario else None
        }
        compras.append(CompraResponse(**compra_dict))
    
    return compras

@router.get("/compras/{compra_id}", response_model=CompraResponse)
async def obtener_compra(
    compra_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene una compra por ID"""
    compra = db.query(Compra).filter(Compra.id == compra_id).first()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    
    proveedor = db.query(Proveedor).filter(Proveedor.id == compra.proveedor_id).first()
    local = db.query(Local).filter(Local.id == compra.local_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == compra.usuario_id).first() if compra.usuario_id else None
    
    return CompraResponse(
        id=compra.id,
        folio=compra.folio,
        factura=compra.factura,
        fecha=compra.fecha,
        proveedor_id=compra.proveedor_id,
        local_id=compra.local_id,
        estado=compra.estado.value if compra.estado else "pendiente",
        total=compra.total,
        subtotal=compra.subtotal,
        descuento=compra.descuento,
        iva=compra.iva,
        notas=compra.notas,
        tipo_moneda=compra.tipo_moneda,
        usuario_id=compra.usuario_id,
        fecha_creacion=compra.fecha_creacion,
        fecha_actualizacion=compra.fecha_actualizacion,
        proveedor_nombre=proveedor.nombre if proveedor else None,
        local_nombre=local.nombre if local else None,
        usuario_nombre=usuario.nombre_completo if usuario else None
    )

@router.post("/compras", response_model=CompraResponse, status_code=201)
async def crear_compra(
    compra: CompraCreate,
    db: Session = Depends(get_db)
):
    """Crea una nueva compra"""
    # Verificar si ya existe una compra con el mismo folio
    existe = db.query(Compra).filter(Compra.folio == compra.folio).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una compra con este folio")
    
    # Crear compra
    estado_enum = EstadoCompra[compra.estado.upper()] if compra.estado else EstadoCompra.PENDIENTE
    db_compra = Compra(
        folio=compra.folio,
        factura=compra.factura,
        fecha=compra.fecha,
        proveedor_id=compra.proveedor_id,
        local_id=compra.local_id,
        estado=estado_enum,
        total=compra.total,
        subtotal=compra.subtotal or 0,
        descuento=compra.descuento or 0,
        iva=compra.iva or 0,
        notas=compra.notas,
        tipo_moneda=compra.tipo_moneda or "pesos",
        usuario_id=compra.usuario_id
    )
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    
    # Obtener información relacionada
    proveedor = db.query(Proveedor).filter(Proveedor.id == db_compra.proveedor_id).first()
    local = db.query(Local).filter(Local.id == db_compra.local_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == db_compra.usuario_id).first() if db_compra.usuario_id else None
    
    return CompraResponse(
        id=db_compra.id,
        folio=db_compra.folio,
        factura=db_compra.factura,
        fecha=db_compra.fecha,
        proveedor_id=db_compra.proveedor_id,
        local_id=db_compra.local_id,
        estado=db_compra.estado.value if db_compra.estado else "pendiente",
        total=db_compra.total,
        subtotal=db_compra.subtotal,
        descuento=db_compra.descuento,
        iva=db_compra.iva,
        notas=db_compra.notas,
        tipo_moneda=db_compra.tipo_moneda,
        usuario_id=db_compra.usuario_id,
        fecha_creacion=db_compra.fecha_creacion,
        fecha_actualizacion=db_compra.fecha_actualizacion,
        proveedor_nombre=proveedor.nombre if proveedor else None,
        local_nombre=local.nombre if local else None,
        usuario_nombre=usuario.nombre_completo if usuario else None
    )
