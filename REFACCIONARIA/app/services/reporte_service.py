from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.models.venta import Venta, EstadoVenta, DetalleVenta
from app.models.producto import Producto
from app.models.local import Local
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.schemas.devoluciones_detalladas import DevolucionesDetalladasResponse, DevolucionDetalleResponse


class ReporteService:
    def __init__(self, db: Session):
        self.db = db

    async def generar_reporte_devoluciones_detalladas(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        sucursal: Optional[str] = None,
        vendedor: Optional[str] = None,
        folio: Optional[str] = None,
        cliente: Optional[str] = None,
        estado: Optional[str] = None
    ) -> DevolucionesDetalladasResponse:
        """
        Genera reporte de devoluciones detalladas
        """
        try:
            # Convertir fechas a datetime
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            # Ajustar fecha_fin para incluir todo el día
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)

            # Construir query base
            query = self.db.query(
                Venta,
                DetalleVenta,
                Producto,
                Local,
                Usuario,
                Cliente
            ).join(
                DetalleVenta, Venta.id == DetalleVenta.venta_id
            ).join(
                Producto, DetalleVenta.producto_id == Producto.id
            ).join(
                Local, Venta.local_id == Local.id
            ).join(
                Usuario, Venta.usuario_id == Usuario.id
            ).join(
                Cliente, Venta.cliente_id == Cliente.id, isouter=True
            ).filter(
                Venta.estado == EstadoVenta.DEVUELTA,
                Venta.fecha_creacion >= fecha_inicio_dt,
                Venta.fecha_creacion <= fecha_fin_dt
            )

            # Aplicar filtros opcionales
            if sucursal and sucursal != 'all':
                query = query.filter(Local.nombre.ilike(f"%{sucursal}%"))

            if vendedor and vendedor != 'all':
                query = query.filter(
                    or_(
                        Usuario.nombre.ilike(f"%{vendedor}%"),
                        Usuario.nombre_usuario.ilike(f"%{vendedor}%"),
                        Usuario.apellido_paterno.ilike(f"%{vendedor}%"),
                        Usuario.apellido_materno.ilike(f"%{vendedor}%")
                    )
                )

            if folio:
                query = query.filter(Venta.folio.ilike(f"%{folio}%"))

            if cliente:
                query = query.filter(
                    or_(
                        Cliente.nombre.ilike(f"%{cliente}%"),
                        Cliente.apellido_paterno.ilike(f"%{cliente}%"),
                        Cliente.apellido_materno.ilike(f"%{cliente}%"),
                        Cliente.razon_social.ilike(f"%{cliente}%")
                    )
                )

            if estado:
                try:
                    estado_enum = EstadoVenta(estado)
                    query = query.filter(Venta.estado == estado_enum)
                except Exception:
                    pass

            # Ejecutar query
            resultados = query.all()

            # Procesar resultados
            devoluciones = []
            total_monto = 0.0

            for venta, detalle, producto, local, usuario, cliente_db in resultados:
                monto = float(detalle.importe) if detalle.importe else 0.0
                total_monto += monto

                devolucion = DevolucionDetalleResponse(
                    fecha_venta=venta.fecha_creacion.strftime("%Y-%m-%d") if venta.fecha_creacion else "-",
                    fecha_devolucion=venta.fecha_modificacion.strftime("%Y-%m-%d") if venta.fecha_modificacion else venta.fecha_creacion.strftime("%Y-%m-%d") if venta.fecha_creacion else "-",
                    sucursal=local.nombre if local else "-",
                    vendedor=usuario.nombre_completo if usuario else "-",
                    folio=venta.folio if venta.folio else "-",
                    producto=f"{producto.nombre} ({producto.codigo})" if producto else "-",
                    monto=str(monto),
                    cliente=cliente_db.nombre_completo if cliente_db else "PUBLICO GENERAL",
                    estado=venta.estado.value if venta.estado else "-",
                    total=float(venta.total or monto)
                )
                devoluciones.append(devolucion)

            return DevolucionesDetalladasResponse(
                total=len(devoluciones),
                devoluciones=devoluciones,
                total_monto=total_monto
            )

        except Exception as e:
            raise Exception(f"Error al generar reporte de devoluciones: {str(e)}")

    async def generar_reporte_ventas_diarias(self, fecha: str = None, local_id: int = None):
        """
        Genera reporte de ventas diarias
        """
        # Implementación básica - puede expandirse según necesidades
        return {
            "fecha": fecha or datetime.now().strftime("%Y-%m-%d"),
            "total_ventas": 0,
            "total_monto": 0.0
        }
