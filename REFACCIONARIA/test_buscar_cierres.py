import sys
sys.path.insert(0, '.')
from app.core.database import SessionLocal
from app.services.cierre_caja_service import CierreCajaService

db = SessionLocal()
servicio = CierreCajaService(db)

# Buscar como lo hace el frontend
print("🔍 Buscando cierres del 5-6 de febrero con caja='ventas10' y vendedor='administrador':")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    caja='ventas10',
    vendedor='administrador',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  - {c}")

print("\n🔍 Buscando SIN FILTRO de caja ni vendedor:")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  - Caja: {c.caja}, Vendedor: {c.vendedor}")

print("\n🔍 Buscando solo por caja='ventas10':")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    caja='ventas10',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  - Caja: {c.caja}, Vendedor: {c.vendedor}")

db.close()
