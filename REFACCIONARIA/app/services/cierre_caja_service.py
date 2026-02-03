# app/services/cierre_caja_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Optional
from app.models.venta import Venta
from app.models.usuario import Usuario
from app.models.local import Local
from app.schemas.cierre_caja import CierreCajaResponse, CierreCajaCreate, CierreCajaOut
from app.models.cierre_caja import CierreCaja

class CierreCajaService:
    def __init__(self, db: Session):
        self.db = db
    
    def obtener_cierres(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        caja: Optional[str] = None,
        vendedor: Optional[str] = None,
        local_id: Optional[int] = None
    ) -> List[CierreCajaResponse]:
        """
        Obtiene los cierres de caja con filtros opcionales
        
        Args:
            fecha_inicio: Fecha de inicio en formato YYYY-MM-DD
            fecha_fin: Fecha de fin en formato YYYY-MM-DD
            caja: Número o nombre de caja (opcional)
            vendedor: Nombre del vendedor (opcional)
            local_id: ID del local (opcional)
        
        Returns:
            Lista de cierres de caja
        """
        try:
            # Convertir fechas
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
            
            # Consulta base desde la tabla cierres_caja
            query = self.db.query(
                CierreCaja.caja,
                Usuario.nombre.label('vendedor'),
                CierreCaja.fecha_creacion.label('fecha_cierre'),
                CierreCaja.total_cierre
            ).join(
                Usuario, CierreCaja.usuario_id == Usuario.id
            ).filter(
                and_(
                    CierreCaja.fecha_creacion >= fecha_inicio_dt,
                    CierreCaja.fecha_creacion <= fecha_fin_dt
                )
            )
            
            # Filtro por caja
            if caja:
                query = query.filter(CierreCaja.caja.ilike(f"%{caja}%"))
            
            # Filtro por vendedor
            if vendedor:
                query = query.filter(Usuario.nombre.ilike(f"%{vendedor}%"))
            
            # Filtro por local
            if local_id:
                query = query.filter(CierreCaja.local_id == local_id)
            
            # Ordenar por fecha de creación descendente (más recientes primero)
            query = query.order_by(CierreCaja.fecha_creacion.desc())
            
            resultados = query.all()
            
            # Formatear resultados
            cierres = []
            for resultado in resultados:
                fecha_cierre = resultado.fecha_cierre
                cierre = CierreCajaResponse(
                    caja=resultado.caja,
                    vendedor=resultado.vendedor,
                    apertura=fecha_cierre.strftime("%d/%m/%Y") if fecha_cierre else "",
                    hora_apertura=fecha_cierre.strftime("%H:%M") if fecha_cierre else "",
                    cierre=fecha_cierre.strftime("%d/%m/%Y") if fecha_cierre else "",
                    hora_cierre=fecha_cierre.strftime("%H:%M") if fecha_cierre else "",
                    total_cierre=float(resultado.total_cierre or 0)
                )
                cierres.append(cierre)
            
            return cierres
            
        except Exception as e:
            print(f"Error en obtener_cierres: {str(e)}")
            return []
    
    def obtener_estadisticas_cierre(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        local_id: Optional[int] = None
    ) -> dict:
        """
        Obtiene estadísticas de cierres de caja
        """
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
            
            query = self.db.query(Venta).filter(
                and_(
                    Venta.fecha_creacion >= fecha_inicio_dt,
                    Venta.fecha_creacion <= fecha_fin_dt
                )
            )
            
            if local_id:
                query = query.filter(Venta.local_id == local_id)
            
            ventas = query.all()
            
            total_ventas = len(ventas)
            total_ingresos = sum(float(venta.total) for venta in ventas) if ventas else 0
            total_descuentos = sum(float(venta.descuento) for venta in ventas) if ventas else 0

            # Estadísticas por método de pago (conteo y suma)
            por_metodo_pago = {}
            query_mp = self.db.query(
                Venta.metodo_pago.label('metodo'),
                func.count(Venta.id).label('conteo'),
                func.sum(Venta.total).label('suma')
            ).filter(
                and_(
                    Venta.fecha_creacion >= fecha_inicio_dt,
                    Venta.fecha_creacion <= fecha_fin_dt
                )
            )
            if local_id:
                query_mp = query_mp.filter(Venta.local_id == local_id)
            query_mp = query_mp.group_by(Venta.metodo_pago)
            for metodo, conteo, suma in query_mp.all():
                por_metodo_pago[str(metodo or 'desconocido')] = {
                    'conteo': int(conteo or 0),
                    'total': float(suma or 0)
                }

            # Estadísticas por vendedor (conteo y suma)
            por_vendedor = {}
            query_v = self.db.query(
                Usuario.nombre.label('vendedor'),
                func.count(Venta.id).label('conteo'),
                func.sum(Venta.total).label('suma')
            ).join(Usuario, Venta.usuario_id == Usuario.id).filter(
                and_(
                    Venta.fecha_creacion >= fecha_inicio_dt,
                    Venta.fecha_creacion <= fecha_fin_dt
                )
            )
            if local_id:
                query_v = query_v.filter(Venta.local_id == local_id)
            query_v = query_v.group_by(Usuario.nombre)
            for vendedor, conteo, suma in query_v.all():
                por_vendedor[str(vendedor or 'N/A')] = {
                    'conteo': int(conteo or 0),
                    'total': float(suma or 0)
                }
            
            return {
                "total_ventas": total_ventas,
                "total_ingresos": total_ingresos,
                "total_descuentos": total_descuentos,
                "promedio_venta": total_ingresos / total_ventas if total_ventas > 0 else 0,
                "por_metodo_pago": por_metodo_pago,
                "por_vendedor": por_vendedor
            }
            
        except Exception as e:
            print(f"Error en obtener_estadisticas_cierre: {str(e)}")
            return {}

    def crear_cierre(self, data: CierreCajaCreate) -> CierreCajaOut:
        """Crea y guarda un cierre de caja a partir de los montos capturados."""
        try:
            ingresos = (
                float(data.efectivo) + float(data.cheque) + float(data.tarjeta) +
                float(data.debito) + float(data.deposito) + float(data.credito) +
                float(data.vale) + float(data.lealtad)
            )
            total_cierre = ingresos - float(data.retiros)

            cierre = CierreCaja(
                caja=data.caja,
                local_id=data.local_id,
                usuario_id=data.usuario_id,
                efectivo=data.efectivo or 0,
                cheque=data.cheque or 0,
                tarjeta=data.tarjeta or 0,
                debito=data.debito or 0,
                deposito=data.deposito or 0,
                credito=data.credito or 0,
                vale=data.vale or 0,
                lealtad=data.lealtad or 0,
                retiros=data.retiros or 0,
                total_ingresos=ingresos,
                total_cierre=total_cierre
            )

            self.db.add(cierre)
            self.db.commit()
            self.db.refresh(cierre)

            return CierreCajaOut.model_validate(cierre)
        except Exception as e:
            self.db.rollback()
            raise e

    def listar_cierres(
        self,
        fecha_inicio=None,
        fecha_fin=None,
        caja: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CierreCajaOut]:
        """Lista los cierres de caja con filtros opcionales"""
        try:
            query = self.db.query(CierreCaja)
            
            if fecha_inicio:
                query = query.filter(func.date(CierreCaja.fecha_creacion) >= fecha_inicio)
            
            if fecha_fin:
                query = query.filter(func.date(CierreCaja.fecha_creacion) <= fecha_fin)
            
            if caja:
                query = query.filter(CierreCaja.caja.ilike(f"%{caja}%"))
            
            query = query.order_by(CierreCaja.fecha_creacion.desc())
            query = query.offset(skip).limit(limit)
            
            cierres = query.all()
            return [CierreCajaOut.model_validate(c) for c in cierres]
        except Exception as e:
            print(f"Error en listar_cierres: {str(e)}")
            return []
