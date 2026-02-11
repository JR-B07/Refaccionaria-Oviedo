from app.core.database import SessionLocal
from app.models.devolucion_compra import DevolucionCompra

db = SessionLocal()
count = db.query(DevolucionCompra).count()
print(f'Total de devoluciones de compra: {count}')

# Mostrar las primeras si existen
if count > 0:
    devoluciones = db.query(DevolucionCompra).all()
    for dev in devoluciones[:3]:
        print(f' - ID: {dev.id}, Folio: {dev.folio}, Fecha: {dev.fecha_devolucion}, Local: {dev.local_id}')
else:
    print('No hay devoluciones de compra en la base de datos')

db.close()
