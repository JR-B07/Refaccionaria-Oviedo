import sys
import json
sys.path.insert(0, '.')
from app.core.database import SessionLocal
from app.services.cierre_caja_service import CierreCajaService
from app.schemas.cierre_caja import CierreCajaListResponse

db = SessionLocal()
servicio = CierreCajaService(db)

# Test 1: Sin filtros
print("=== TEST 1: SIN FILTROS ===")
print("Parámetros: fecha_inicio='2026-02-05', fecha_fin='2026-02-06', local_id=1")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  ✓ Caja: {c.caja}, Vendedor: {c.vendedor}")

# Test 2: Con filtro de caja
print("\n=== TEST 2: CON FILTRO DE CAJA ===")
print("Parámetros: caja='ventas10', fecha_inicio='2026-02-05', fecha_fin='2026-02-06', local_id=1")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    caja='ventas10',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  ✓ Caja: {c.caja}, Vendedor: {c.vendedor}")

# Test 3: Con filtro de vendedor
print("\n=== TEST 3: CON FILTRO DE VENDEDOR ===")
print("Parámetros: vendedor='Administrador', fecha_inicio='2026-02-05', fecha_fin='2026-02-06', local_id=1")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    vendedor='Administrador',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  ✓ Caja: {c.caja}, Vendedor: {c.vendedor}")

# Test 4: Con ambos filtros
print("\n=== TEST 4: CON AMBOS FILTROS ===")
print("Parámetros: caja='ventas10', vendedor='Administrador', fecha_inicio='2026-02-05', fecha_fin='2026-02-06', local_id=1")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    caja='ventas10',
    vendedor='Administrador',
    local_id=1
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  ✓ Caja: {c.caja}, Vendedor: {c.vendedor}")
    print(f"    Apertura: {c.apertura} {c.hora_apertura}")
    print(f"    Total: ${c.total_cierre}")

# Test 5: Sucursal 2
print("\n=== TEST 5: SUCURSAL 2 ===")
print("Parámetros: fecha_inicio='2026-02-05', fecha_fin='2026-02-06', local_id=2")
cierres = servicio.obtener_cierres(
    fecha_inicio='2026-02-05',
    fecha_fin='2026-02-06',
    local_id=2
)
print(f"Resultados: {len(cierres)}")
for c in cierres:
    print(f"  ✓ Caja: {c.caja}, Vendedor: {c.vendedor}")

db.close()
print("\n✅ Todos los Tests completados")
