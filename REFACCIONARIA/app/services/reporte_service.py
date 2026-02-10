from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.models.venta import Venta, EstadoVenta, DetalleVenta
from app.models.devolucion_compra import DevolucionCompra
from app.models.producto import Producto
from app.models.local import Local
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.proveedor import Proveedor
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
                DetalleVenta, Venta.id == DetalleVenta.venta_id, isouter=True
            ).join(
                Producto, DetalleVenta.producto_id == Producto.id, isouter=True
            ).join(
                Local, Venta.local_id == Local.id
            ).join(
                Usuario, Venta.usuario_id == Usuario.id
            ).join(
                Cliente, Venta.cliente_id == Cliente.id, isouter=True
            ).filter(
                Venta.estado == "devuelta",
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
                # Filtrar por estado usando string directamente
                query = query.filter(Venta.estado == estado.lower())

            # Ejecutar query
            resultados = query.all()

            # Procesar resultados
            devoluciones = []
            total_monto = 0.0

            for venta, detalle, producto, local, usuario, cliente_db in resultados:
                # Calcular monto (usar total de venta si no hay detalle)
                if detalle and detalle.importe:
                    monto = float(detalle.importe)
                else:
                    monto = float(venta.total) if venta.total else 0.0
                
                total_monto += monto

                # Construir nombre del producto
                if producto:
                    producto_str = f"{producto.nombre} ({producto.codigo})"
                else:
                    producto_str = "SIN DETALLES"

                devolucion = DevolucionDetalleResponse(
                    fecha_venta=venta.fecha_creacion.strftime("%Y-%m-%d") if venta.fecha_creacion else "-",
                    fecha_devolucion=venta.fecha_actualizacion.strftime("%Y-%m-%d") if venta.fecha_actualizacion else venta.fecha_creacion.strftime("%Y-%m-%d") if venta.fecha_creacion else "-",
                    sucursal=local.nombre if local else "-",
                    vendedor=usuario.nombre_completo if usuario else "-",
                    folio=venta.folio if venta.folio else "-",
                    producto=producto_str,
                    monto=str(monto),
                    cliente=cliente_db.nombre_completo if cliente_db else "PUBLICO GENERAL",
                    estado=venta.estado if venta.estado else "-",
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

    async def generar_reporte_devoluciones_compra(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        sucursal: Optional[str] = None,
        proveedor: Optional[str] = None,
        folio: Optional[str] = None,
        estado: Optional[str] = None
    ) -> DevolucionesDetalladasResponse:
        """
        Genera reporte de devoluciones de compra detalladas
        """
        try:
            # Convertir fechas a datetime
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            # Ajustar fecha_fin para incluir todo el día
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)

            # Construir query base para devoluciones de compra
            query = self.db.query(
                DevolucionCompra,
                Local,
                Usuario,
                Proveedor
            ).join(
                Local, DevolucionCompra.local_id == Local.id
            ).join(
                Usuario, DevolucionCompra.usuario_id == Usuario.id
            ).join(
                Proveedor, DevolucionCompra.proveedor_id == Proveedor.id, isouter=True
            ).filter(
                DevolucionCompra.fecha_devolucion >= fecha_inicio_dt.date(),
                DevolucionCompra.fecha_devolucion <= fecha_fin_dt.date()
            )

            # Aplicar filtros opcionales
            if sucursal and sucursal != 'all':
                query = query.filter(Local.nombre.ilike(f"%{sucursal}%"))

            if proveedor and proveedor != 'all':
                query = query.filter(Proveedor.nombre.ilike(f"%{proveedor}%"))

            if folio:
                query = query.filter(DevolucionCompra.folio.ilike(f"%{folio}%"))

            if estado:
                query = query.filter(DevolucionCompra.estado == estado.lower())

            # Ejecutar query
            resultados = query.all()

            # Procesar resultados
            devoluciones = []
            total_monto = 0.0

            for dev_compra, local, usuario, proveedor_db in resultados:
                monto = float(dev_compra.monto_total) if dev_compra.monto_total else 0.0
                total_monto += monto

                # Construir nombre del producto
                producto_str = f"{dev_compra.producto_nombre}"

                devolucion = DevolucionDetalleResponse(
                    fecha_venta=dev_compra.fecha_devolucion.strftime("%Y-%m-%d") if dev_compra.fecha_devolucion else "-",
                    fecha_devolucion=dev_compra.fecha_devolucion.strftime("%Y-%m-%d") if dev_compra.fecha_devolucion else "-",
                    sucursal=local.nombre if local else "-",
                    vendedor=usuario.nombre_completo if usuario else "-",
                    folio=dev_compra.folio if dev_compra.folio else "-",
                    producto=producto_str,
                    monto=str(monto),
                    cliente=proveedor_db.nombre if proveedor_db else "SIN PROVEEDOR",
                    estado=dev_compra.estado if dev_compra.estado else "-",
                    total=monto
                )
                devoluciones.append(devolucion)

            return DevolucionesDetalladasResponse(
                total=len(devoluciones),
                devoluciones=devoluciones,
                total_monto=total_monto
            )

        except Exception as e:
            raise Exception(f"Error al generar reporte de devoluciones de compra: {str(e)}")

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
