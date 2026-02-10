#!/usr/bin/env python
# Script para insertar ventas de prueba en febrero 2026
from app.core.database import SessionLocal
from app.models.venta import Venta, EstadoVenta, TipoVenta
from datetime import datetime, timedelta

db = SessionLocal()

# Eliminar ventas de 2026 si existen
ventas_2026 = db.query(Venta).filter(Venta.fecha_creacion >= datetime(2026, 1, 1)).all()
print(f"Eliminando {len(ventas_2026)} ventas de 2026...")
for v in ventas_2026:
    db.delete(v)
db.commit()

# Crear ventas para cada día de febrero 2026
ventas_por_crear = [
    # Semana 1
    (datetime(2026, 2, 1, 10, 30), 150.00),
    (datetime(2026, 2, 1, 14, 15), 200.50),
    (datetime(2026, 2, 2, 9, 45), 120.75),
    (datetime(2026, 2, 2, 16, 20), 180.00),
    (datetime(2026, 2, 3, 11, 10), 90.25),
    (datetime(2026, 2, 3, 15, 30), 250.00),
    (datetime(2026, 2, 4, 10, 00), 165.50),
    (datetime(2026, 2, 4, 17, 45), 210.75),
    (datetime(2026, 2, 5, 9, 30), 320.00),  # Hoy
    (datetime(2026, 2, 5, 13, 20), 145.25),  # Hoy
    
    # Semana 2
    (datetime(2026, 2, 8, 10, 15), 275.00),
    (datetime(2026, 2, 9, 14, 30), 198.50),
    (datetime(2026, 2, 10, 11, 45), 235.75),
    (datetime(2026, 2, 11, 15, 00), 189.00),
    (datetime(2026, 2, 12, 9, 30), 310.25),
    
    # Semana 3
    (datetime(2026, 2, 15, 12, 00), 155.00),
    (datetime(2026, 2, 16, 10, 30), 220.50),
    (datetime(2026, 2, 17, 14, 15), 275.00),
    (datetime(2026, 2, 18, 11, 45), 195.75),
    (datetime(2026, 2, 19, 15, 00), 265.25),
    
    # Semana 4
    (datetime(2026, 2, 22, 9, 00), 185.00),
    (datetime(2026, 2, 23, 13, 30), 310.50),
    (datetime(2026, 2, 24, 10, 15), 245.75),
    (datetime(2026, 2, 25, 14, 45), 175.00),
    (datetime(2026, 2, 26, 11, 30), 295.25),
    
    # Últimos días
    (datetime(2026, 2, 27, 15, 00), 220.00),
    (datetime(2026, 2, 28, 10, 30), 310.75),
]

folio_base = 100000
for i, (fecha, total) in enumerate(ventas_por_crear):
    venta = Venta(
        folio=f"V-{folio_base + i}",
        local_id=1,
        usuario_id=3,
        cliente_id=None,
        tipo_venta=TipoVenta.CONTADO,
        estado=EstadoVenta.COMPLETADA,
        subtotal=total * 0.85,  # 85% del total
        descuento=0,
        iva=total * 0.15,  # 15% de IVA
        total=total,
        pago_recibido=total,
        cambio=0,
        metodo_pago="efectivo",
        fecha_creacion=fecha
    )
    db.add(venta)
    print(f"  ✓ {venta.folio} - ${venta.total} - {fecha.strftime('%Y-%m-%d %H:%M')}")

db.commit()
print(f"\n✓ {len(ventas_por_crear)} ventas de prueba insertadas en febrero 2026")

# Verificar
resultado = db.query(Venta).filter(
    Venta.fecha_creacion >= datetime(2026, 2, 1),
    Venta.fecha_creacion < datetime(2026, 3, 1)
).count()
print(f"Verificación: {resultado} ventas en febrero 2026")

db.close()
