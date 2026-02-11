from app.core.database import SessionLocal
from app.models.venta import Venta
from datetime import datetime

db = SessionLocal()

# Rango Feb 2026
fecha_inicio = datetime(2026, 1, 1)
fecha_fin = datetime(2026, 3, 1)

# Contar devueltas en rango
count = db.query(Venta).filter(
    Venta.estado == "devuelta",
    Venta.fecha_creacion >= fecha_inicio,
    Venta.fecha_creacion <= fecha_fin
).count()

print(f"✅ Ventas devueltas en Enero-Febrero 2026: {count}")

if count > 0:
    print("✅ Ahora deberías poder ver datos en el reporte")
else:
    print("❌ Aún no hay datos")

db.close()
