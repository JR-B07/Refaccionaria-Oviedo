# app/api/v1/endpoints/inventario.py
from typing import List, Optional, Any
from app.api.deps import get_current_user

# --- Listado de inventario filtrado por sucursal del usuario autenticado ---
@router.get("/inventario", tags=["Inventario"])
async def listar_inventario(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Listar inventario SOLO de la sucursal del usuario autenticado
    """
    from app.models.producto import InventarioLocal
    local_id = current_user["local_id"]
    query = db.query(InventarioLocal).filter(InventarioLocal.local_id == local_id)
    inventario = query.offset(skip).limit(limit).all()
    return inventario
async def ajustar_inventario(
    ajuste: AjusteInventarioCreate,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ajuste manual de inventario
    Motivos: daño, robo, error, etc.
    """
    # Registrar movimiento
    movimiento = MovimientoInventario(
        producto_id=ajuste.producto_id,
        local_id=ajuste.local_id,
        tipo="ajuste",
        cantidad=ajuste.cantidad_nueva - ajuste.cantidad_anterior,
        motivo=ajuste.motivo,
        usuario_id=usuario_id
    )
    db.add(movimiento)
    db.commit()
    
    return {"message": "Inventario ajustado correctamente"}

@router.post("/inventario/transferir")
async def transferir_entre_locales(
    transferencia: TransferenciaCreate,
    db: Session = Depends(get_db)
):
    """
    Transferir productos entre locales
    Ej: 10 llantas del local 1 al local 2
    """
    servicio = InventarioService(db)
    return await servicio.transferir_productos(transferencia)