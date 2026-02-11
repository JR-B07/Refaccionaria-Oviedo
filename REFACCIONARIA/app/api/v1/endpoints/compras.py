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
    db: Session = Depends(get_db)
):
    """
    Lista compras con filtros opcionales
    Sin autenticación requerida (compatible con acceso público)
    """
    # Sin autenticación, retornar todas las compras
    query = db.query(Compra)

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
        
        # Manejar estado que puede ser enum o string
        estado_valor = compra.estado if isinstance(compra.estado, str) else (compra.estado.value if compra.estado else "pendiente")
        
        # Convertir datetime a date si es necesario
        fecha_valor = compra.fecha.date() if hasattr(compra.fecha, 'date') else compra.fecha
        
        compra_dict = {
            "id": compra.id,
            "folio": compra.folio,
            "factura": compra.factura,
            "fecha": fecha_valor,
            "proveedor_id": compra.proveedor_id,
            "local_id": compra.local_id,
            "estado": estado_valor,
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
    
    # Manejar estado que puede ser enum o string
    estado_valor = compra.estado if isinstance(compra.estado, str) else (compra.estado.value if compra.estado else "pendiente")
    
    return CompraResponse(
        id=compra.id,
        folio=compra.folio,
        factura=compra.factura,
        fecha=compra.fecha,
        proveedor_id=compra.proveedor_id,
        local_id=compra.local_id,
        estado=estado_valor,
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
    try:
        # Verificar si ya existe una compra con el mismo folio
        existe = db.query(Compra).filter(Compra.folio == compra.folio).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe una compra con este folio")
        
        # Validar que el proveedor existe
        proveedor = db.query(Proveedor).filter(Proveedor.id == compra.proveedor_id).first()
        if not proveedor:
            raise HTTPException(status_code=400, detail=f"Proveedor con ID {compra.proveedor_id} no encontrado")
        
        # Validar que el local existe
        local = db.query(Local).filter(Local.id == compra.local_id).first()
        if not local:
            raise HTTPException(status_code=400, detail=f"Local con ID {compra.local_id} no encontrado")
        
        # Validar usuario si se proporciona
        usuario = None
        if compra.usuario_id:
            usuario = db.query(Usuario).filter(Usuario.id == compra.usuario_id).first()
            if not usuario:
                raise HTTPException(status_code=400, detail=f"Usuario con ID {compra.usuario_id} no encontrado")
        
        # Normalizar estado
        estado_valor = (compra.estado or "pendiente").lower()
        
        db_compra = Compra(
            folio=compra.folio,
            factura=compra.factura,
            fecha=compra.fecha if hasattr(compra.fecha, 'timestamp') else datetime.combine(compra.fecha, datetime.min.time()) if compra.fecha else datetime.now(),
            proveedor_id=compra.proveedor_id,
            local_id=compra.local_id,
            estado=estado_valor,  # Guardar directamente como string
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
        
        # Retornar respuesta
        return CompraResponse(
            id=db_compra.id,
            folio=db_compra.folio,
            factura=db_compra.factura,
            fecha=db_compra.fecha,
            proveedor_id=db_compra.proveedor_id,
            local_id=db_compra.local_id,
            estado=db_compra.estado if isinstance(db_compra.estado, str) else (db_compra.estado.value if db_compra.estado else "pendiente"),
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
            usuario_nombre=usuario.nombre if usuario else None
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear compra: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al crear compra: {str(e)}")

@router.patch("/compras/{compra_id}/estado")
async def actualizar_estado_compra(
    compra_id: int,
    nuevo_estado: str = Query(..., description="Nuevo estado: pendiente, completo, cancelado, parcial"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Actualiza el estado de una compra"""
    try:
        # Buscar la compra
        compra = db.query(Compra).filter(Compra.id == compra_id).first()
        if not compra:
            raise HTTPException(status_code=404, detail="Compra no encontrada")
        
        # Verificar permisos: solo administradores pueden cambiar otros usuarios, o gerentes su propia sucursal
        if current_user.get("rol") == "administrador" or current_user.get("rol") == "superadministrador":
            pass  # Admin puede cambiar cualquiera
        elif compra.local_id != current_user.get("local_id"):
            raise HTTPException(status_code=403, detail="No tienes permisos para modificar esta compra")
        
        # Validar estado
        estado_normalizado = nuevo_estado.lower()
        estados_validos = ["pendiente", "completo", "cancelado", "parcial"]
        if estado_normalizado not in estados_validos:
            raise HTTPException(
                status_code=400, 
                detail=f"Estado inválido. Valores permitidos: {', '.join(estados_validos)}"
            )
        
        # Actualizar estado
        compra.estado = estado_normalizado
        compra.fecha_actualizacion = datetime.utcnow()
        db.commit()
        db.refresh(compra)
        
        return {
            "success": True,
            "message": f"Estado actualizado a: {estado_normalizado}",
            "estado": compra.estado,
            "id": compra.id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al actualizar estado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar estado: {str(e)}")
