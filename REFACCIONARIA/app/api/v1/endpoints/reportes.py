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
@router.get("/reportes/estadisticas-ventas")
async def estadisticas_ventas(
    tipo: str = "anual",
    anio: int = 2026,
    mes: int = None,
    local_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas de ventas para gráficas.
    
    Parámetros:
    - tipo: 'anual', 'mensual' o 'diaria'
    - anio: Año para filtrar
    - mes: Mes (solo para tipo='diaria')
    - local_id: ID del local (opcional)
    """
    from app.models.venta import Venta, EstadoVenta
    from sqlalchemy import func, extract
    from datetime import datetime
    
    try:
        query = db.query(
            Venta.total,
            func.count(Venta.id).label('cantidad')
        ).filter(Venta.estado == EstadoVenta.COMPLETADA)
        
        if local_id:
            query = query.filter(Venta.local_id == local_id)
        
        if tipo == 'anual':
            # Datos por año (últimos 7 años)
            query_result = db.query(
                extract('year', Venta.fecha_creacion).label('year'),
                func.sum(Venta.total).label('total_ventas'),
                func.count(Venta.id).label('cantidad')
            ).filter(Venta.estado == EstadoVenta.COMPLETADA)
            
            if local_id:
                query_result = query_result.filter(Venta.local_id == local_id)
            
            query_result = query_result.group_by('year').order_by('year').all()
            
            años = []
            ventas = []
            cantidades = []
            for row in query_result:
                if row[0]:
                    años.append(str(int(row[0])))
                    ventas.append(float(row[1] or 0))
                    cantidades.append(int(row[2] or 0))
            
            # Si hay menos de 7 años, agregar años vacíos
            while len(años) < 7:
                años.insert(0, str(2026 - len(años)))
                ventas.insert(0, 0)
                cantidades.insert(0, 0)
            
            return {
                "labels": años[-7:],
                "ventas": ventas[-7:],
                "cantidad": cantidades[-7:]
            }
        
        elif tipo == 'mensual':
            # Datos por mes del año actual
            query_result = db.query(
                extract('month', Venta.fecha_creacion).label('mes'),
                func.sum(Venta.total).label('total_ventas'),
                func.count(Venta.id).label('cantidad')
            ).filter(
                extract('year', Venta.fecha_creacion) == anio,
                Venta.estado == EstadoVenta.COMPLETADA
            )
            
            if local_id:
                query_result = query_result.filter(Venta.local_id == local_id)
            
            query_result = query_result.group_by('mes').order_by('mes').all()
            
            meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            ventas = [0] * 12
            cantidades = [0] * 12
            
            for row in query_result:
                if row[0]:
                    mes_idx = int(row[0]) - 1
                    ventas[mes_idx] = float(row[1] or 0)
                    cantidades[mes_idx] = int(row[2] or 0)
            
            return {
                "labels": meses,
                "ventas": ventas,
                "cantidad": cantidades
            }
        
        elif tipo == 'diaria':
            # Datos diarios del mes actual
            if not mes:
                mes = datetime.now().month
            
            query_result = db.query(
                extract('day', Venta.fecha_creacion).label('dia'),
                func.sum(Venta.total).label('total_ventas'),
                func.count(Venta.id).label('cantidad')
            ).filter(
                extract('year', Venta.fecha_creacion) == anio,
                extract('month', Venta.fecha_creacion) == mes,
                Venta.estado == EstadoVenta.COMPLETADA
            )
            
            if local_id:
                query_result = query_result.filter(Venta.local_id == local_id)
            
            query_result = query_result.group_by('dia').order_by('dia').all()
            
            dias = list(range(1, 32))
            ventas = [0] * 31
            cantidades = [0] * 31
            
            for row in query_result:
                if row[0]:
                    dia_idx = int(row[0]) - 1
                    ventas[dia_idx] = float(row[1] or 0)
                    cantidades[dia_idx] = int(row[2] or 0)
            
            return {
                "labels": [str(d) for d in dias],
                "ventas": ventas,
                "cantidad": cantidades
            }
        
        else:
            raise HTTPException(status_code=400, detail="Tipo inválido")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))