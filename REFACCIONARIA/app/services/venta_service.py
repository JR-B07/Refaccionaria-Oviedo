# app/services/venta_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.venta import Venta, DetalleVenta, EstadoVenta, TipoVenta
from app.models.inventario_local import InventarioLocal
from app.schemas.venta import VentaCreate, VentaResponse
from datetime import datetime
from typing import Optional

class VentaService:
    """Servicio para gestionar operaciones de ventas"""
    
    model_class = Venta
    
    def __init__(self, db: Session):
        self.db = db
    
    async def procesar_venta(self, venta_data: VentaCreate) -> VentaResponse:
        """
        Procesa una venta rápida:
        1. Valida que los datos sean correctos
        2. Crea la venta en la BD
        3. Registra los detalles de venta
        4. Actualiza el inventario local
        5. Retorna la venta creada
        """
        try:
            # Convertir tipo_venta a enum
            tipo_venta_str = venta_data.tipo_venta.upper() if isinstance(venta_data.tipo_venta, str) else venta_data.tipo_venta
            if tipo_venta_str == 'CONTADO':
                tipo_venta_enum = TipoVenta.CONTADO
            elif tipo_venta_str == 'CREDITO':
                tipo_venta_enum = TipoVenta.CREDITO
            elif tipo_venta_str == 'APARTADO':
                tipo_venta_enum = TipoVenta.APARTADO
            else:
                tipo_venta_enum = TipoVenta.CONTADO
            
            # Convertir estado a enum
            estado_str = venta_data.estado.lower()
            if estado_str == "completada":
                estado_enum = EstadoVenta.COMPLETADA
            elif estado_str == "pendiente":
                estado_enum = EstadoVenta.PENDIENTE
            elif estado_str == "cancelada":
                estado_enum = EstadoVenta.CANCELADA
            elif estado_str == "devuelta":
                estado_enum = EstadoVenta.DEVUELTA
            else:
                estado_enum = EstadoVenta.PENDIENTE
            
            # Crear la venta
            nueva_venta = Venta(
                folio=venta_data.folio,
                local_id=venta_data.local_id,
                usuario_id=venta_data.usuario_id,
                cliente_id=venta_data.cliente_id,
                tipo_venta=tipo_venta_enum,
                estado=estado_enum,
                subtotal=float(venta_data.subtotal),
                descuento=float(venta_data.descuento),
                iva=float(venta_data.iva),
                total=float(venta_data.total),
                pago_recibido=float(venta_data.pago_recibido),
                cambio=float(venta_data.cambio),
                metodo_pago=venta_data.metodo_pago,
                fecha_limite_pago=venta_data.fecha_limite_pago,
                saldo_pendiente=float(venta_data.saldo_pendiente),
                fecha_creacion=datetime.now()
            )
            
            self.db.add(nueva_venta)
            self.db.flush()  # Flush para obtener el ID sin commit
            
            # Registrar detalles de venta si existen
            if venta_data.detalles:
                for detalle_data in venta_data.detalles:
                    detalle = DetalleVenta(
                        venta_id=nueva_venta.id,
                        producto_id=detalle_data.producto_id,
                        local_id=venta_data.local_id,
                        cantidad=detalle_data.cantidad,
                        precio_unitario=float(detalle_data.precio_unitario),
                        descuento=float(detalle_data.descuento),
                        importe=float(detalle_data.importe)
                    )
                    self.db.add(detalle)
            
            # Commit de toda la transacción
            self.db.commit()
            self.db.refresh(nueva_venta)
            
            return VentaResponse.from_orm(nueva_venta)
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al procesar venta: {str(e)}")
    
    def obtener_venta_por_folio(self, folio: str) -> Optional[Venta]:
        """Obtiene una venta por su folio"""
        return self.db.query(Venta).filter(Venta.folio == folio).first()
    
    def obtener_ventas_por_local(self, local_id: int, skip: int = 0, limit: int = 100):
        """Obtiene ventas de un local específico"""
        return self.db.query(Venta).filter(
            Venta.local_id == local_id
        ).order_by(Venta.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    def obtener_total_ventas_dia(self, local_id: int, fecha: datetime):
        """Obtiene el total de ventas en un día específico"""
        inicio_dia = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
        fin_dia = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)
        
        resultado = self.db.query(
            func.count(Venta.id).label('cantidad'),
            func.sum(Venta.total).label('total_monto')
        ).filter(
            Venta.local_id == local_id,
            Venta.estado == EstadoVenta.COMPLETADA,
            Venta.fecha_creacion >= inicio_dia,
            Venta.fecha_creacion <= fin_dia
        ).first()
        
        return {
            'cantidad': resultado.cantidad or 0,
            'total': float(resultado.total_monto or 0)
        }
