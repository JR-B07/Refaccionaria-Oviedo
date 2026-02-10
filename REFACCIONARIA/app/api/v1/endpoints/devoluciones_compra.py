from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.core.database import get_db
from app.models.devolucion_compra import DevolucionCompra
from app.models.proveedor import Proveedor
from app.models.local import Local
from app.models.usuario import Usuario
from app.schemas.devolucion_compra import (
    DevolucionCompraResponse, 
    DevolucionCompraCreate,
    DevolucionCompraUpdate
)

router = APIRouter()

@router.get("/devoluciones-compra", response_model=List[DevolucionCompraResponse])
async def listar_devoluciones_compra(
    folio: Optional[str] = Query(None, description="Folio de la devolución"),
    factura: Optional[str] = Query(None, description="Número de factura"),
    proveedor_id: Optional[int] = Query(None, description="ID del proveedor"),
    local_id: Optional[int] = Query(None, description="ID del local"),
    estado: Optional[str] = Query(None, description="Estado de la devolución"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista devoluciones de compra con filtros opcionales
    Sin autenticación requerida (compatible con acceso público)
    """
    query = db.query(DevolucionCompra)

    # Aplicar filtros
    if folio:
        query = query.filter(DevolucionCompra.folio.ilike(f"%{folio}%"))
    if factura:
        query = query.filter(DevolucionCompra.factura.ilike(f"%{factura}%"))
    if proveedor_id:
        query = query.filter(DevolucionCompra.proveedor_id == proveedor_id)
    if local_id:
        query = query.filter(DevolucionCompra.local_id == local_id)
    if estado:
        query = query.filter(DevolucionCompra.estado == estado)
    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            query = query.filter(DevolucionCompra.fecha_devolucion >= fecha_inicio_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_inicio inválido. Use YYYY-MM-DD")
    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            query = query.filter(DevolucionCompra.fecha_devolucion <= fecha_fin_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_fin inválido. Use YYYY-MM-DD")

    # Ordenar por fecha descendente
    query = query.order_by(DevolucionCompra.fecha_devolucion.desc())

    # Ejecutar query
    devoluciones_db = query.offset(skip).limit(limit).all()
    
    # Formatear respuesta con joins
    devoluciones = []
    for dev in devoluciones_db:
        # Obtener nombres de relaciones
        proveedor = db.query(Proveedor).filter(Proveedor.id == dev.proveedor_id).first() if dev.proveedor_id else None
        local = db.query(Local).filter(Local.id == dev.local_id).first()
        usuario = db.query(Usuario).filter(Usuario.id == dev.usuario_id).first()
        
        # Manejar estado que puede ser enum o string
        estado_valor = dev.estado if isinstance(dev.estado, str) else (dev.estado.value if dev.estado else "pendiente")
        
        # Convertir fecha_devolucion a string YYYY-MM-DD
        fecha_str = dev.fecha_devolucion.strftime("%Y-%m-%d") if isinstance(dev.fecha_devolucion, date) else str(dev.fecha_devolucion)
        
        devolucion_dict = {
            "id": dev.id,
            "folio": dev.folio,
            "compra_id": dev.compra_id,
            "factura": dev.factura,
            "proveedor_id": dev.proveedor_id,
            "proveedor_nombre": proveedor.nombre if proveedor else None,
            "estado": estado_valor,
            "fecha_devolucion": fecha_str,
            "nota_credito": dev.nota_credito,
            "producto_nombre": dev.producto_nombre,
            "cantidad": dev.cantidad,
            "precio_unitario": float(dev.precio_unitario) if dev.precio_unitario else 0.0,
            "monto_total": float(dev.monto_total) if dev.monto_total else 0.0,
            "descripcion": dev.descripcion,
            "local_id": dev.local_id,
            "local_nombre": local.nombre if local else None,
            "usuario_id": dev.usuario_id,
            "usuario_nombre": usuario.nombre_completo if usuario else None,
            "fecha_creacion": dev.fecha_creacion,
            "fecha_actualizacion": dev.fecha_actualizacion
        }
        
        devoluciones.append(devolucion_dict)
    
    return devoluciones


@router.get("/devoluciones-compra/{devolucion_id}", response_model=DevolucionCompraResponse)
async def obtener_devolucion_compra(
    devolucion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una devolución de compra por su ID
    """
    dev = db.query(DevolucionCompra).filter(DevolucionCompra.id == devolucion_id).first()
    
    if not dev:
        raise HTTPException(status_code=404, detail="Devolución de compra no encontrada")
    
    # Obtener nombres de relaciones
    proveedor = db.query(Proveedor).filter(Proveedor.id == dev.proveedor_id).first() if dev.proveedor_id else None
    local = db.query(Local).filter(Local.id == dev.local_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == dev.usuario_id).first()
    
    # Manejar estado
    estado_valor = dev.estado if isinstance(dev.estado, str) else (dev.estado.value if dev.estado else "pendiente")
    
    # Convertir fecha_devolucion a string
    fecha_str = dev.fecha_devolucion.strftime("%Y-%m-%d") if isinstance(dev.fecha_devolucion, date) else str(dev.fecha_devolucion)
    
    return {
        "id": dev.id,
        "folio": dev.folio,
        "compra_id": dev.compra_id,
        "factura": dev.factura,
        "proveedor_id": dev.proveedor_id,
        "proveedor_nombre": proveedor.nombre if proveedor else None,
        "estado": estado_valor,
        "fecha_devolucion": fecha_str,
        "nota_credito": dev.nota_credito,
        "producto_nombre": dev.producto_nombre,
        "cantidad": dev.cantidad,
        "precio_unitario": float(dev.precio_unitario) if dev.precio_unitario else 0.0,
        "monto_total": float(dev.monto_total) if dev.monto_total else 0.0,
        "descripcion": dev.descripcion,
        "local_id": dev.local_id,
        "local_nombre": local.nombre if local else None,
        "usuario_id": dev.usuario_id,
        "usuario_nombre": usuario.nombre_completo if usuario else None,
        "fecha_creacion": dev.fecha_creacion,
        "fecha_actualizacion": dev.fecha_actualizacion
    }


@router.post("/devoluciones-compra", response_model=DevolucionCompraResponse)
async def crear_devolucion_compra(
    devolucion: DevolucionCompraCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva devolución de compra
    """
    # Validar que el proveedor existe si se proporciona
    if devolucion.proveedor_id:
        proveedor = db.query(Proveedor).filter(Proveedor.id == devolucion.proveedor_id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Validar que el local existe
    local = db.query(Local).filter(Local.id == devolucion.local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # Validar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == devolucion.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validar unicidad del folio
    folio_existente = db.query(DevolucionCompra).filter(DevolucionCompra.folio == devolucion.folio).first()
    if folio_existente:
        raise HTTPException(status_code=400, detail=f"Ya existe una devolución con el folio {devolucion.folio}")
    
    # Convertir fecha string a date object si es necesario
    fecha_dev = devolucion.fecha_devolucion
    if isinstance(fecha_dev, str):
        try:
            fecha_dev = datetime.strptime(fecha_dev, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_devolucion inválido. Use YYYY-MM-DD")
    
    # Crear nueva devolución
    nueva_devolucion = DevolucionCompra(
        folio=devolucion.folio,
        compra_id=devolucion.compra_id,
        factura=devolucion.factura,
        proveedor_id=devolucion.proveedor_id,
        estado=devolucion.estado,
        fecha_devolucion=fecha_dev,
        nota_credito=devolucion.nota_credito,
        producto_nombre=devolucion.producto_nombre,
        cantidad=devolucion.cantidad,
        precio_unitario=devolucion.precio_unitario,
        monto_total=devolucion.monto_total,
        descripcion=devolucion.descripcion,
        local_id=devolucion.local_id,
        usuario_id=devolucion.usuario_id
    )
    
    db.add(nueva_devolucion)
    db.commit()
    db.refresh(nueva_devolucion)
    
    # Retornar con nombres de relaciones
    proveedor = db.query(Proveedor).filter(Proveedor.id == nueva_devolucion.proveedor_id).first() if nueva_devolucion.proveedor_id else None
    local = db.query(Local).filter(Local.id == nueva_devolucion.local_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == nueva_devolucion.usuario_id).first()
    
    estado_valor = nueva_devolucion.estado if isinstance(nueva_devolucion.estado, str) else (nueva_devolucion.estado.value if nueva_devolucion.estado else "pendiente")
    fecha_str = nueva_devolucion.fecha_devolucion.strftime("%Y-%m-%d") if isinstance(nueva_devolucion.fecha_devolucion, date) else str(nueva_devolucion.fecha_devolucion)
    
    return {
        "id": nueva_devolucion.id,
        "folio": nueva_devolucion.folio,
        "compra_id": nueva_devolucion.compra_id,
        "factura": nueva_devolucion.factura,
        "proveedor_id": nueva_devolucion.proveedor_id,
        "proveedor_nombre": proveedor.nombre if proveedor else None,
        "estado": estado_valor,
        "fecha_devolucion": fecha_str,
        "nota_credito": nueva_devolucion.nota_credito,
        "producto_nombre": nueva_devolucion.producto_nombre,
        "cantidad": nueva_devolucion.cantidad,
        "precio_unitario": float(nueva_devolucion.precio_unitario),
        "monto_total": float(nueva_devolucion.monto_total),
        "descripcion": nueva_devolucion.descripcion,
        "local_id": nueva_devolucion.local_id,
        "local_nombre": local.nombre if local else None,
        "usuario_id": nueva_devolucion.usuario_id,
        "usuario_nombre": usuario.nombre_completo if usuario else None,
        "fecha_creacion": nueva_devolucion.fecha_creacion,
        "fecha_actualizacion": nueva_devolucion.fecha_actualizacion
    }


@router.put("/devoluciones-compra/{devolucion_id}", response_model=DevolucionCompraResponse)
async def actualizar_devolucion_compra(
    devolucion_id: int,
    devolucion_update: DevolucionCompraUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una devolución de compra existente
    """
    # Buscar la devolución
    dev = db.query(DevolucionCompra).filter(DevolucionCompra.id == devolucion_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Devolución de compra no encontrada")
    
    # Actualizar campos proporcionados
    update_data = devolucion_update.model_dump(exclude_unset=True)
    
    # Validar folio único si se está actualizando
    if "folio" in update_data and update_data["folio"] != dev.folio:
        folio_existente = db.query(DevolucionCompra).filter(
            DevolucionCompra.folio == update_data["folio"],
            DevolucionCompra.id != devolucion_id
        ).first()
        if folio_existente:
            raise HTTPException(status_code=400, detail=f"Ya existe otra devolución con el folio {update_data['folio']}")
    
    # Validar proveedor si se actualiza
    if "proveedor_id" in update_data and update_data["proveedor_id"]:
        proveedor = db.query(Proveedor).filter(Proveedor.id == update_data["proveedor_id"]).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Validar local si se actualiza
    if "local_id" in update_data:
        local = db.query(Local).filter(Local.id == update_data["local_id"]).first()
        if not local:
            raise HTTPException(status_code=404, detail="Local no encontrado")
    
    # Validar usuario si se actualiza
    if "usuario_id" in update_data:
        usuario = db.query(Usuario).filter(Usuario.id == update_data["usuario_id"]).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Convertir fecha si viene como string
    if "fecha_devolucion" in update_data and isinstance(update_data["fecha_devolucion"], str):
        try:
            update_data["fecha_devolucion"] = datetime.strptime(update_data["fecha_devolucion"], "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_devolucion inválido. Use YYYY-MM-DD")
    
    # Aplicar actualizaciones
    for campo, valor in update_data.items():
        setattr(dev, campo, valor)
    
    db.commit()
    db.refresh(dev)
    
    # Retornar con nombres de relaciones
    proveedor = db.query(Proveedor).filter(Proveedor.id == dev.proveedor_id).first() if dev.proveedor_id else None
    local = db.query(Local).filter(Local.id == dev.local_id).first()
    usuario = db.query(Usuario).filter(Usuario.id == dev.usuario_id).first()
    
    estado_valor = dev.estado if isinstance(dev.estado, str) else (dev.estado.value if dev.estado else "pendiente")
    fecha_str = dev.fecha_devolucion.strftime("%Y-%m-%d") if isinstance(dev.fecha_devolucion, date) else str(dev.fecha_devolucion)
    
    return {
        "id": dev.id,
        "folio": dev.folio,
        "compra_id": dev.compra_id,
        "factura": dev.factura,
        "proveedor_id": dev.proveedor_id,
        "proveedor_nombre": proveedor.nombre if proveedor else None,
        "estado": estado_valor,
        "fecha_devolucion": fecha_str,
        "nota_credito": dev.nota_credito,
        "producto_nombre": dev.producto_nombre,
        "cantidad": dev.cantidad,
        "precio_unitario": float(dev.precio_unitario),
        "monto_total": float(dev.monto_total),
        "descripcion": dev.descripcion,
        "local_id": dev.local_id,
        "local_nombre": local.nombre if local else None,
        "usuario_id": dev.usuario_id,
        "usuario_nombre": usuario.nombre_completo if usuario else None,
        "fecha_creacion": dev.fecha_creacion,
        "fecha_actualizacion": dev.fecha_actualizacion
    }


@router.delete("/devoluciones-compra/{devolucion_id}")
async def eliminar_devolucion_compra(
    devolucion_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una devolución de compra
    """
    dev = db.query(DevolucionCompra).filter(DevolucionCompra.id == devolucion_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Devolución de compra no encontrada")
    
    folio = dev.folio
    
    db.delete(dev)
    db.commit()
    
    return {"message": f"Devolución {folio} eliminada exitosamente", "id": devolucion_id}
