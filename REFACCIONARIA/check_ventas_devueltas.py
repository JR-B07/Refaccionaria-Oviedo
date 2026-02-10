from app.core.database import SessionLocal
from app.models.venta import Venta
from datetime import datetime

db = SessionLocal()

# Contar ventas devueltas en general
devueltas_total = db.query(Venta).filter(Venta.estado == "devuelta").count()
print(f'Total de ventas devueltas: {devueltas_total}')

# Mostrar las primeras con sus fechas
if devueltas_total > 0:
    ventas_dev = db.query(Venta).filter(Venta.estado == "devuelta").all()
    for venta in ventas_dev[:5]:
        fecha = venta.fecha_creacion
        print(f' - ID: {venta.id}, Folio: {venta.folio}, Fecha: {fecha}, Estado: {venta.estado}')

print()

# Verificar rango de fechas del reporte: 07/01/2026 - 10/02/2026
fecha_inicio = datetime.strptime('07/01/2026', '%m/%d/%Y')
fecha_fin = datetime.strptime('10/02/2026', '%m/%d/%Y')
fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)

print(f'Buscando devueltas en rango: {fecha_inicio} a {fecha_fin}')

devueltas_rango = db.query(Venta).filter(
    Venta.estado == "devuelta",
    Venta.fecha_creacion >= fecha_inicio,
    Venta.fecha_creacion <= fecha_fin
).count()

print(f'Vendtas devueltas en rango: {devueltas_rango}')

# Mostrar ventas en el rango (todas)
print(f'\nVentas creadas en el rango (todas, no solo devueltas):')
ventas_rango = db.query(Venta).filter(
    Venta.fecha_creacion >= fecha_inicio,
    Venta.fecha_creacion <= fecha_fin
).all()
print(f'Total: {len(ventas_rango)}')
for venta in ventas_rango[:5]:
    print(f' - ID: {venta.id}, Folio: {venta.folio}, Fecha: {venta.fecha_creacion}, Estado: {venta.estado}')

db.close()
