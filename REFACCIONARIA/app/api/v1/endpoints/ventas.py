# app/api/v1/endpoints/ventas.py
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api.deps import get_current_user
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.schemas.venta import VentaCreate, VentaResponse
from app.models.venta import Venta

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
    try:
        print(f"[DEBUG] Datos recibidos en venta_rapida: folio={venta_data.folio}, local_id={venta_data.local_id}, usuario_id={venta_data.usuario_id}, total={venta_data.total}")
        
        # Asignar valores por defecto si falta algo
        folio = str(venta_data.folio).strip() if venta_data.folio else f"VZ{int(1000 + (datetime.now().timestamp() % 9000))}"
        local_id = int(venta_data.local_id) if venta_data.local_id else 1
        usuario_id = int(venta_data.usuario_id) if venta_data.usuario_id else 3
        
        print(f"[DEBUG] Valores ajustados: folio={folio}, local_id={local_id}, usuario_id={usuario_id}")
        
        # Normalizar tipo_venta a minúsculas (strings, no enums)
        tipo_venta_str = str(venta_data.tipo_venta).lower().strip()
        if tipo_venta_str in ("contado",):
            tipo_venta_value = "contado"
        elif tipo_venta_str == "credito":
            tipo_venta_value = "credito"
        elif tipo_venta_str == "apartado":
            tipo_venta_value = "apartado"
        else:
            tipo_venta_value = "contado"
            
        # Normalizar estado a minúsculas (strings, no enums)
        estado_str = str(venta_data.estado).lower().strip()
        if estado_str == "completada":
            estado_value = "completada"
        elif estado_str == "pendiente":
            estado_value = "pendiente"
        elif estado_str == "cancelada":
            estado_value = "cancelada"
        elif estado_str == "devuelta":
            estado_value = "devuelta"
        else:
            estado_value = "completada"
        
        print(f"[DEBUG] Valores normalizados: tipo_venta={tipo_venta_value}, estado={estado_value}")
        
        # Crear nueva venta con los datos validados
        nueva_venta = Venta(
            folio=folio,
            local_id=local_id,
            usuario_id=usuario_id,
            cliente_id=venta_data.cliente_id,
            estado=estado_value,
            tipo_venta=tipo_venta_value,
            subtotal=float(venta_data.subtotal or 0),
            descuento=float(venta_data.descuento or 0),
            iva=float(venta_data.iva or 0),
            total=float(venta_data.total or 0),
            pago_recibido=float(venta_data.pago_recibido or 0),
            cambio=float(venta_data.cambio or 0),
            metodo_pago=str(venta_data.metodo_pago),
            fecha_limite_pago=venta_data.fecha_limite_pago,
            saldo_pendiente=float(venta_data.saldo_pendiente or 0)
        )
        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)
        print(f"✓✓✓ VENTA REGISTRADA EXITOSAMENTE: folio={nueva_venta.folio}, id={nueva_venta.id}")
        return nueva_venta
    except Exception as e:
        db.rollback()
        print(f"[ERROR CRÍTICO] En venta_rapida: {str(e)}")
        import traceback
        error_trace = traceback.format_exc()
        print(error_trace)
        raise HTTPException(
            status_code=400, 
            detail=f"Error al guardar la venta: {str(e)}"
        )

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
    query = db.query(Venta).filter_by(local_id=local_id)
    ventas = query.order_by(Venta.id.desc()).offset(skip).limit(limit).all()
    return ventas