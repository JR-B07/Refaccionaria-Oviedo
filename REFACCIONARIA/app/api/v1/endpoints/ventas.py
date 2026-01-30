# app/api/v1/endpoints/ventas.py
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.schemas.venta import VentaCreate, VentaResponse
from app.services.venta_service import VentaService

router = APIRouter()

@router.post("/ventas/rapida", response_model=VentaResponse)
async def venta_rapida(
    venta_data: VentaCreate,
    db: Session = Depends(get_db)
):
    """
    Venta rápida para caja
    - Valida stock en tiempo real
    - Actualiza inventario
    - Genera folio automático
    - Calcula cambio automático
    """
    servicio = VentaService(db)
    return await servicio.procesar_venta(venta_data)

# --- Listado de ventas filtrado por sucursal del usuario autenticado ---
@router.get("/ventas", response_model=List[VentaResponse])
async def listar_ventas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Listar ventas SOLO de la sucursal del usuario autenticado
    """
    local_id = current_user["local_id"]
    query = db.query(VentaService.model_class).filter_by(local_id=local_id)
    ventas = query.order_by(VentaService.model_class.id.desc()).offset(skip).limit(limit).all()
    return ventas

@router.get("/ventas/consulta/{codigo_barras}")
async def consultar_producto(
    codigo_barras: str,
    local_id: int,
    db: Session = Depends(get_db)
):
    """Consulta rápida de producto por código de barras"""
    from app.crud.producto import producto_crud
    
    producto = producto_crud.get_by_codigo_barras(db, codigo_barras)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    
    # Verificar stock en el local específico
    stock_local = db.query(InventarioLocal).filter(
        InventarioLocal.producto_id == producto.id,
        InventarioLocal.local_id == local_id
    ).first()
    
    return {
        "producto": producto,
        "stock_local": stock_local.stock if stock_local else 0,
        "precio_venta": producto.precio_venta,
        "compatibilidad": producto.compatibilidad
    }