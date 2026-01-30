from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cierre_caja import CierreCajaResponse, CierreCajaListResponse
from app.schemas.devoluciones_detalladas import DevolucionesDetalladasResponse
from app.services.cierre_caja_service import CierreCajaService
from app.services.reporte_service import ReporteService

router = APIRouter()

@router.get("/reportes/cierres-caja", response_model=CierreCajaListResponse)
async def obtener_cierres_caja(
    fecha_inicio: str,
    fecha_fin: str,
    caja: Optional[str] = None,
    vendedor: Optional[str] = None,
    local_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de cierres de caja con filtros opcionales
    
    Parámetros:
    - fecha_inicio: Fecha en formato YYYY-MM-DD
    - fecha_fin: Fecha en formato YYYY-MM-DD
    - caja: Número de caja (opcional)
    - vendedor: Nombre del vendedor (opcional)
    - local_id: ID del local (opcional)
    """
    try:
        servicio = CierreCajaService(db)
        cierres = servicio.obtener_cierres(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            caja=caja,
            vendedor=vendedor,
            local_id=local_id
        )
        
        return CierreCajaListResponse(
            total=len(cierres),
            cierres=cierres
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reportes/cierres-caja/estadisticas")
async def estadisticas_cierres_caja(
    fecha_inicio: str,
    fecha_fin: str,
    local_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Estadísticas agregadas de cierres/ventas en el período indicado."""
    try:
        servicio = CierreCajaService(db)
        stats = servicio.obtener_estadisticas_cierre(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            local_id=local_id
        )
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reportes/devoluciones-detalladas", response_model=DevolucionesDetalladasResponse)
async def reporte_devoluciones_detalladas(
    fecha_inicio: str,
    fecha_fin: str,
    sucursal: Optional[str] = None,
    vendedor: Optional[str] = None,
    folio: Optional[str] = None,
    cliente: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Reporte detallado de devoluciones por fecha
    
    Parámetros:
    - fecha_inicio: Fecha en formato YYYY-MM-DD
    - fecha_fin: Fecha en formato YYYY-MM-DD
    - sucursal: Nombre de la sucursal (opcional)
    - vendedor: Nombre del vendedor (opcional)
    """
    try:
        servicio = ReporteService(db)
        return await servicio.generar_reporte_devoluciones_detalladas(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            sucursal=sucursal,
            vendedor=vendedor,
            folio=folio,
            cliente=cliente,
            estado=estado
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reportes/ventas-diarias")
async def reporte_ventas_diarias(
    fecha: str = None,
    local_id: int = None,
    db: Session = Depends(get_db)
):
    """Reporte de ventas del día con gráficos"""
    from app.services.reporte_service import ReporteService
    
    servicio = ReporteService(db)
    return await servicio.generar_reporte_ventas_diarias(fecha, local_id)

@router.get("/reportes/productos-mas-vendidos")
async def productos_mas_vendidos(
    fecha_inicio: str,
    fecha_fin: str,
    limite: int = 10,
    db: Session = Depends(get_db)
):
    """Top 10 productos más vendidos en período"""
    query = """
    SELECT p.nombre, p.codigo, SUM(dv.cantidad) as total_vendido
    FROM detalle_ventas dv
    JOIN productos p ON dv.producto_id = p.id
    JOIN ventas v ON dv.venta_id = v.id
    WHERE v.fecha_creacion BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.id
    ORDER BY total_vendido DESC
    LIMIT :limite
    """
    
    result = db.execute(query, {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "limite": limite
    }).fetchall()
    
    return result
