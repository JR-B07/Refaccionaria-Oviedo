from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.core.database import get_db
from app.models.vale_venta import ValeVenta
from app.models.usuario import Usuario
from app.models.local import Local
from app.schemas.vale_venta import ValeVentaCreate, ValeVentaUpdate, ValeVentaResponse

router = APIRouter()

@router.get("/vales-venta", response_model=List[ValeVentaResponse])
async def listar_vales_venta(
    folio: Optional[str] = Query(None, description="Folio o descripción"),
    vendedor_id: Optional[int] = Query(None, description="ID del vendedor"),
    monto_aproximado: Optional[float] = Query(None, description="Monto aproximado"),
    local_id: Optional[int] = Query(None, description="ID de la sucursal"),
    tipo: Optional[str] = Query(None, description="venta o devolucion"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD"),
    disponible: Optional[bool] = Query(None, description="Filtrar por disponible"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista vales de venta con filtros opcionales"""
    query = db.query(
        ValeVenta,
        Usuario,
        Local
    ).join(
        Usuario, ValeVenta.vendedor_id == Usuario.id
    ).join(
        Local, ValeVenta.local_id == Local.id
    )

    # Aplicar filtros
    if folio:
        query = query.filter(
            or_(
                ValeVenta.folio.ilike(f"%{folio}%"),
                ValeVenta.descripcion.ilike(f"%{folio}%")
            )
        )
    
    if vendedor_id:
        query = query.filter(ValeVenta.vendedor_id == vendedor_id)
    
    if monto_aproximado:
        # Buscar montos cercanos (±10%)
        monto_min = monto_aproximado * 0.9
        monto_max = monto_aproximado * 1.1
        query = query.filter(
            and_(
                ValeVenta.monto >= monto_min,
                ValeVenta.monto <= monto_max
            )
        )
    
    if local_id:
        query = query.filter(ValeVenta.local_id == local_id)
    
    if tipo:
        # Convertir string a Enum - aceptar tanto minúsculas como mayúsculas
        from app.models.vale_venta import TipoVale
        try:
            tipo_enum = TipoVale[tipo.upper()]
            query = query.filter(ValeVenta.tipo == tipo_enum)
        except (KeyError, AttributeError):
            # Si no es válido, ignorar el filtro
            pass
    
    if fecha_inicio:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        query = query.filter(ValeVenta.fecha >= fecha_inicio_dt)
    
    if fecha_fin:
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        query = query.filter(ValeVenta.fecha <= fecha_fin_dt)
    
    if disponible is not None:
        query = query.filter(ValeVenta.disponible == disponible)

    # Ejecutar query
    resultados = query.offset(skip).limit(limit).all()
    
    # Formatear respuesta
    vales = []
    for vale, usuario, local in resultados:
        vale_dict = {
            "id": vale.id,
            "folio": vale.folio,
            "monto": vale.monto,
            "concepto": vale.concepto,
            "fecha": vale.fecha,
            "vendedor_id": vale.vendedor_id,
            "local_id": vale.local_id,
            "usado": vale.usado,
            "fecha_uso": vale.fecha_uso,
            "destino": vale.destino,
            "tipo": vale.tipo.value if vale.tipo else "venta",
            "disponible": vale.disponible,
            "descripcion": vale.descripcion,
            "venta_origen_id": vale.venta_origen_id,
            "fecha_creacion": vale.fecha_creacion,
            "fecha_actualizacion": vale.fecha_actualizacion,
            "vendedor_nombre": usuario.nombre_completo if usuario else None,
            "local_nombre": local.nombre if local else None
        }
        vales.append(ValeVentaResponse(**vale_dict))
    
    return vales

@router.get("/vales-venta/{vale_id}", response_model=ValeVentaResponse)
async def obtener_vale_venta(
    vale_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un vale de venta por ID"""
    vale = db.query(ValeVenta).filter(ValeVenta.id == vale_id).first()
    if not vale:
        raise HTTPException(status_code=404, detail="Vale de venta no encontrado")
    
    usuario = db.query(Usuario).filter(Usuario.id == vale.vendedor_id).first()
    local = db.query(Local).filter(Local.id == vale.local_id).first()
    
    return ValeVentaResponse(
        id=vale.id,
        folio=vale.folio,
        monto=vale.monto,
        concepto=vale.concepto,
        fecha=vale.fecha,
        vendedor_id=vale.vendedor_id,
        local_id=vale.local_id,
        usado=vale.usado,
        fecha_uso=vale.fecha_uso,
        destino=vale.destino,
        tipo=vale.tipo.value if vale.tipo else "venta",
        disponible=vale.disponible,
        descripcion=vale.descripcion,
        venta_origen_id=vale.venta_origen_id,
        fecha_creacion=vale.fecha_creacion,
        fecha_actualizacion=vale.fecha_actualizacion,
        vendedor_nombre=usuario.nombre_completo if usuario else None,
        local_nombre=local.nombre if local else None
    )

@router.post("/vales-venta", response_model=ValeVentaResponse, status_code=201)
async def crear_vale_venta(
    vale: ValeVentaCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo vale de venta"""
    # Verificar si ya existe un vale con el mismo folio
    existe = db.query(ValeVenta).filter(ValeVenta.folio == vale.folio).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un vale con este folio")
    
    from app.models.vale_venta import TipoVale
    
    # El schema ya normalizó tipo a mayúsculas
    # Convertir a enum
    tipo_vale = TipoVale.VENTA
    if vale.tipo:
        if vale.tipo == "DEVOLUCION":
            tipo_vale = TipoVale.DEVOLUCION
        elif vale.tipo == "VENTA":
            tipo_vale = TipoVale.VENTA
    
    # Crear el objeto ValeVenta
    db_vale = ValeVenta(
        folio=vale.folio,
        monto=vale.monto,
        concepto=vale.concepto or "POR ANTICIPO",
        fecha=vale.fecha,
        vendedor_id=vale.vendedor_id,
        local_id=vale.local_id,
        tipo=tipo_vale,
        disponible=vale.disponible if vale.disponible is not None else True,
        descripcion=vale.descripcion,
        venta_origen_id=vale.venta_origen_id,
        usado=False
    )

    # Validar relaciones existentes
    if not db.query(Usuario).filter(Usuario.id == db_vale.vendedor_id).first():
        raise HTTPException(status_code=400, detail="Vendedor no existe")
    if not db.query(Local).filter(Local.id == db_vale.local_id).first():
        raise HTTPException(status_code=400, detail="Sucursal no existe")

    db.add(db_vale)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el vale: {str(e)}")
    db.refresh(db_vale)
    
    # Obtener información relacionada
    usuario = db.query(Usuario).filter(Usuario.id == db_vale.vendedor_id).first()
    local = db.query(Local).filter(Local.id == db_vale.local_id).first()
    
    return ValeVentaResponse(
        id=db_vale.id,
        folio=db_vale.folio,
        monto=db_vale.monto,
        concepto=db_vale.concepto,
        fecha=db_vale.fecha,
        vendedor_id=db_vale.vendedor_id,
        local_id=db_vale.local_id,
        usado=db_vale.usado,
        fecha_uso=db_vale.fecha_uso,
        destino=db_vale.destino,
        tipo=db_vale.tipo.value if db_vale.tipo else "venta",
        disponible=db_vale.disponible,
        descripcion=db_vale.descripcion,
        venta_origen_id=db_vale.venta_origen_id,
        fecha_creacion=db_vale.fecha_creacion,
        fecha_actualizacion=db_vale.fecha_actualizacion,
        vendedor_nombre=usuario.nombre_completo if usuario else None,
        local_nombre=local.nombre if local else None
    )

@router.put("/vales-venta/{vale_id}", response_model=ValeVentaResponse)
async def actualizar_vale_venta(
    vale_id: int,
    vale: ValeVentaUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un vale de venta existente"""
    db_vale = db.query(ValeVenta).filter(ValeVenta.id == vale_id).first()
    if not db_vale:
        raise HTTPException(status_code=404, detail="Vale de venta no encontrado")
    
    # Verificar si el folio ya existe en otro vale
    if vale.folio and vale.folio != db_vale.folio:
        existe = db.query(ValeVenta).filter(
            ValeVenta.folio == vale.folio,
            ValeVenta.id != vale_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe otro vale con este folio")
    
    # Actualizar solo los campos proporcionados
    update_data = vale.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vale, field, value)
    
    db.commit()
    db.refresh(db_vale)
    
    # Obtener información relacionada
    usuario = db.query(Usuario).filter(Usuario.id == db_vale.vendedor_id).first()
    local = db.query(Local).filter(Local.id == db_vale.local_id).first()
    
    return ValeVentaResponse(
        id=db_vale.id,
        folio=db_vale.folio,
        monto=db_vale.monto,
        concepto=db_vale.concepto,
        fecha=db_vale.fecha,
        vendedor_id=db_vale.vendedor_id,
        local_id=db_vale.local_id,
        usado=db_vale.usado,
        fecha_uso=db_vale.fecha_uso,
        destino=db_vale.destino,
        tipo=db_vale.tipo.value if db_vale.tipo else "venta",
        disponible=db_vale.disponible,
        descripcion=db_vale.descripcion,
        venta_origen_id=db_vale.venta_origen_id,
        fecha_creacion=db_vale.fecha_creacion,
        fecha_actualizacion=db_vale.fecha_actualizacion,
        vendedor_nombre=usuario.nombre_completo if usuario else None,
        local_nombre=local.nombre if local else None
    )

@router.delete("/vales-venta/{vale_id}", status_code=204)
async def eliminar_vale_venta(
    vale_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un vale de venta"""
    db_vale = db.query(ValeVenta).filter(ValeVenta.id == vale_id).first()
    if not db_vale:
        raise HTTPException(status_code=404, detail="Vale de venta no encontrado")
    
    db.delete(db_vale)
    db.commit()
    return None
