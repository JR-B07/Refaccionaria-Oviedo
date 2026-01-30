from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.core.database import get_db
from app.models.traspaso import Traspaso, DetalleTraspaso, EstadoTraspaso
from app.models.local import Local
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.schemas.traspaso import TraspasoCreate, TraspasoUpdate, TraspasoResponse, DetalleTraspasoCreate, DetalleTraspasoResponse

router = APIRouter()

@router.get("/traspasos", response_model=List[TraspasoResponse])
async def listar_traspasos(
    folio: Optional[str] = Query(None, description="Folio del traspaso"),
    origen_id: Optional[int] = Query(None, description="ID del local origen"),
    destino_id: Optional[int] = Query(None, description="ID del local destino"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD"),
    estado: Optional[str] = Query(None, description="Estado del traspaso"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista traspasos con filtros opcionales"""
    from sqlalchemy.orm import aliased
    
    origen_alias = aliased(Local)
    destino_alias = aliased(Local)
    
    query = db.query(
        Traspaso
    ).join(
        origen_alias, Traspaso.origen_id == origen_alias.id
    ).join(
        destino_alias, Traspaso.destino_id == destino_alias.id
    ).outerjoin(
        Usuario, Traspaso.usuario_id == Usuario.id
    )

    # Aplicar filtros
    if folio:
        query = query.filter(Traspaso.folio.ilike(f"%{folio}%"))
    
    if origen_id:
        query = query.filter(Traspaso.origen_id == origen_id)
    
    if destino_id:
        query = query.filter(Traspaso.destino_id == destino_id)
    
    if estado:
        query = query.filter(Traspaso.estado == estado)
    
    if fecha_inicio:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        query = query.filter(Traspaso.fecha >= fecha_inicio_dt)
    
    if fecha_fin:
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        query = query.filter(Traspaso.fecha <= fecha_fin_dt)

    # Ejecutar query
    traspasos_db = query.offset(skip).limit(limit).all()
    
    # Formatear respuesta
    traspasos = []
    for traspaso in traspasos_db:
        origen = db.query(Local).filter(Local.id == traspaso.origen_id).first()
        destino = db.query(Local).filter(Local.id == traspaso.destino_id).first()
        usuario = db.query(Usuario).filter(Usuario.id == traspaso.usuario_id).first() if traspaso.usuario_id else None
        
        # Obtener detalles
        detalles = db.query(DetalleTraspaso).filter(DetalleTraspaso.traspaso_id == traspaso.id).all()
        detalles_response = []
        for detalle in detalles:
            producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
            detalles_response.append(DetalleTraspasoResponse(
                id=detalle.id,
                traspaso_id=detalle.traspaso_id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                cantidad_enviada=detalle.cantidad_enviada,
                cantidad_recibida=detalle.cantidad_recibida,
                producto_nombre=producto.nombre if producto else None,
                producto_codigo=producto.codigo if producto else None
            ))
        
        traspaso_dict = {
            "id": traspaso.id,
            "folio": traspaso.folio,
            "fecha": traspaso.fecha,
            "origen_id": traspaso.origen_id,
            "destino_id": traspaso.destino_id,
            "estado": traspaso.estado.value if traspaso.estado else "pendiente",
            "notas": traspaso.notas,
            "usuario_id": traspaso.usuario_id,
            "fecha_creacion": traspaso.fecha_creacion,
            "fecha_actualizacion": traspaso.fecha_actualizacion,
            "origen_nombre": origen.nombre if origen else None,
            "destino_nombre": destino.nombre if destino else None,
            "usuario_nombre": usuario.nombre_completo if usuario else None,
            "detalles": detalles_response
        }
        traspasos.append(TraspasoResponse(**traspaso_dict))
    
    return traspasos

@router.get("/traspasos/{traspaso_id}", response_model=TraspasoResponse)
async def obtener_traspaso(
    traspaso_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un traspaso por ID"""
    traspaso = db.query(Traspaso).filter(Traspaso.id == traspaso_id).first()
    if not traspaso:
        raise HTTPException(status_code=404, detail="Traspaso no encontrado")
    
    origen = db.query(Local).filter(Local.id == traspaso.origen_id).first()
    destino = db.query(Local).filter(Local.id == traspaso.destino_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == traspaso.usuario_id).first() if traspaso.usuario_id else None
    
    # Obtener detalles
    detalles = db.query(DetalleTraspaso).filter(DetalleTraspaso.traspaso_id == traspaso.id).all()
    detalles_response = []
    for detalle in detalles:
        producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
        detalles_response.append(DetalleTraspasoResponse(
            id=detalle.id,
            traspaso_id=detalle.traspaso_id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            cantidad_enviada=detalle.cantidad_enviada,
            cantidad_recibida=detalle.cantidad_recibida,
            producto_nombre=producto.nombre if producto else None,
            producto_codigo=producto.codigo if producto else None
        ))
    
    return TraspasoResponse(
        id=traspaso.id,
        folio=traspaso.folio,
        fecha=traspaso.fecha,
        origen_id=traspaso.origen_id,
        destino_id=traspaso.destino_id,
        estado=traspaso.estado.value if traspaso.estado else "pendiente",
        notas=traspaso.notas,
        usuario_id=traspaso.usuario_id,
        fecha_creacion=traspaso.fecha_creacion,
        fecha_actualizacion=traspaso.fecha_actualizacion,
        origen_nombre=origen.nombre if origen else None,
        destino_nombre=destino.nombre if destino else None,
        usuario_nombre=usuario.nombre_completo if usuario else None,
        detalles=detalles_response
    )

@router.post("/traspasos", response_model=TraspasoResponse, status_code=201)
async def crear_traspaso(
    traspaso: TraspasoCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo traspaso"""
    # Verificar si ya existe un traspaso con el mismo folio
    existe = db.query(Traspaso).filter(Traspaso.folio == traspaso.folio).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un traspaso con este folio")
    
    # Verificar que origen y destino sean diferentes
    if traspaso.origen_id == traspaso.destino_id:
        raise HTTPException(status_code=400, detail="El origen y destino no pueden ser el mismo")
    
    # Crear traspaso
    estado_enum = EstadoTraspaso[traspaso.estado.upper()] if traspaso.estado else EstadoTraspaso.PENDIENTE
    db_traspaso = Traspaso(
        folio=traspaso.folio,
        fecha=traspaso.fecha,
        origen_id=traspaso.origen_id,
        destino_id=traspaso.destino_id,
        estado=estado_enum,
        notas=traspaso.notas,
        usuario_id=traspaso.usuario_id
    )
    db.add(db_traspaso)
    db.flush()  # Para obtener el ID
    
    # Crear detalles
    if traspaso.detalles:
        for detalle_data in traspaso.detalles:
            detalle = DetalleTraspaso(
                traspaso_id=db_traspaso.id,
                producto_id=detalle_data.producto_id,
                cantidad=detalle_data.cantidad,
                cantidad_enviada=detalle_data.cantidad_enviada or 0,
                cantidad_recibida=detalle_data.cantidad_recibida or 0
            )
            db.add(detalle)
    
    db.commit()
    db.refresh(db_traspaso)
    
    # Obtener información relacionada
    origen = db.query(Local).filter(Local.id == db_traspaso.origen_id).first()
    destino = db.query(Local).filter(Local.id == db_traspaso.destino_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == db_traspaso.usuario_id).first() if db_traspaso.usuario_id else None
    
    # Obtener detalles
    detalles = db.query(DetalleTraspaso).filter(DetalleTraspaso.traspaso_id == db_traspaso.id).all()
    detalles_response = []
    for detalle in detalles:
        producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
        detalles_response.append(DetalleTraspasoResponse(
            id=detalle.id,
            traspaso_id=detalle.traspaso_id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            cantidad_enviada=detalle.cantidad_enviada,
            cantidad_recibida=detalle.cantidad_recibida,
            producto_nombre=producto.nombre if producto else None,
            producto_codigo=producto.codigo if producto else None
        ))
    
    return TraspasoResponse(
        id=db_traspaso.id,
        folio=db_traspaso.folio,
        fecha=db_traspaso.fecha,
        origen_id=db_traspaso.origen_id,
        destino_id=db_traspaso.destino_id,
        estado=db_traspaso.estado.value if db_traspaso.estado else "pendiente",
        notas=db_traspaso.notas,
        usuario_id=db_traspaso.usuario_id,
        fecha_creacion=db_traspaso.fecha_creacion,
        fecha_actualizacion=db_traspaso.fecha_actualizacion,
        origen_nombre=origen.nombre if origen else None,
        destino_nombre=destino.nombre if destino else None,
        usuario_nombre=usuario.nombre_completo if usuario else None,
        detalles=detalles_response
    )

@router.put("/traspasos/{traspaso_id}", response_model=TraspasoResponse)
async def actualizar_traspaso(
    traspaso_id: int,
    traspaso: TraspasoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un traspaso existente"""
    db_traspaso = db.query(Traspaso).filter(Traspaso.id == traspaso_id).first()
    if not db_traspaso:
        raise HTTPException(status_code=404, detail="Traspaso no encontrado")
    
    # Verificar si el folio ya existe en otro traspaso
    if traspaso.folio and traspaso.folio != db_traspaso.folio:
        existe = db.query(Traspaso).filter(
            Traspaso.folio == traspaso.folio,
            Traspaso.id != traspaso_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe otro traspaso con este folio")
    
    # Verificar origen y destino
    origen_id = traspaso.origen_id or db_traspaso.origen_id
    destino_id = traspaso.destino_id or db_traspaso.destino_id
    if origen_id == destino_id:
        raise HTTPException(status_code=400, detail="El origen y destino no pueden ser el mismo")
    
    # Actualizar solo los campos proporcionados
    update_data = traspaso.dict(exclude_unset=True)
    if 'estado' in update_data:
        update_data['estado'] = EstadoTraspaso[update_data['estado'].upper()]
    
    for field, value in update_data.items():
        setattr(db_traspaso, field, value)
    
    db.commit()
    db.refresh(db_traspaso)
    
    # Obtener información relacionada
    origen = db.query(Local).filter(Local.id == db_traspaso.origen_id).first()
    destino = db.query(Local).filter(Local.id == db_traspaso.destino_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == db_traspaso.usuario_id).first() if db_traspaso.usuario_id else None
    
    # Obtener detalles
    detalles = db.query(DetalleTraspaso).filter(DetalleTraspaso.traspaso_id == db_traspaso.id).all()
    detalles_response = []
    for detalle in detalles:
        producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
        detalles_response.append(DetalleTraspasoResponse(
            id=detalle.id,
            traspaso_id=detalle.traspaso_id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            cantidad_enviada=detalle.cantidad_enviada,
            cantidad_recibida=detalle.cantidad_recibida,
            producto_nombre=producto.nombre if producto else None,
            producto_codigo=producto.codigo if producto else None
        ))
    
    return TraspasoResponse(
        id=db_traspaso.id,
        folio=db_traspaso.folio,
        fecha=db_traspaso.fecha,
        origen_id=db_traspaso.origen_id,
        destino_id=db_traspaso.destino_id,
        estado=db_traspaso.estado.value if db_traspaso.estado else "pendiente",
        notas=db_traspaso.notas,
        usuario_id=db_traspaso.usuario_id,
        fecha_creacion=db_traspaso.fecha_creacion,
        fecha_actualizacion=db_traspaso.fecha_actualizacion,
        origen_nombre=origen.nombre if origen else None,
        destino_nombre=destino.nombre if destino else None,
        usuario_nombre=usuario.nombre_completo if usuario else None,
        detalles=detalles_response
    )

@router.delete("/traspasos/{traspaso_id}", status_code=204)
async def eliminar_traspaso(
    traspaso_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un traspaso"""
    db_traspaso = db.query(Traspaso).filter(Traspaso.id == traspaso_id).first()
    if not db_traspaso:
        raise HTTPException(status_code=404, detail="Traspaso no encontrado")
    
    db.delete(db_traspaso)
    db.commit()
    return None
