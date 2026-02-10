from datetime import date
from app.core.database import SessionLocal
from app.models.devolucion_compra import DevolucionCompra
from app.models.proveedor import Proveedor
from app.models.local import Local
from app.models.usuario import Usuario

db = SessionLocal()

# Obtener registros base
proveedor = db.query(Proveedor).order_by(Proveedor.id.asc()).first()
local = db.query(Local).order_by(Local.id.asc()).first()
usuario = db.query(Usuario).order_by(Usuario.id.asc()).first()

if not proveedor:
    print("❌ No hay proveedores en la base de datos")
    db.close()
    raise SystemExit(1)

if not local:
    print("❌ No hay locales en la base de datos")
    db.close()
    raise SystemExit(1)

if not usuario:
    print("❌ No hay usuarios en la base de datos")
    db.close()
    raise SystemExit(1)

fechas = [
    date(2026, 7, 6),
    date(2026, 8, 12),
    date(2026, 9, 25),
]

creadas = 0
for i, fecha_dev in enumerate(fechas, start=1):
    folio = f"DEV-COMP-2026-{i:04d}"
    # Evitar duplicado por si ya existe
    existe = db.query(DevolucionCompra).filter(DevolucionCompra.folio == folio).first()
    if existe:
        folio = f"{folio}-R"

    cantidad = 2 + i
    precio_unitario = 150.0 + (i * 25.0)
    monto_total = cantidad * precio_unitario

    devolucion = DevolucionCompra(
        folio=folio,
        compra_id=None,
        factura=f"FAC-2026-{100+i}",
        proveedor_id=proveedor.id,
        estado="pendiente",
        fecha_devolucion=fecha_dev,
        nota_credito=f"NC-2026-{200+i}",
        producto_nombre=f"PRODUCTO PRUEBA {i}",
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        monto_total=monto_total,
        descripcion="Devolucion de compra de prueba",
        local_id=local.id,
        usuario_id=usuario.id,
    )

    db.add(devolucion)
    creadas += 1
    print(f"✅ Devolucion compra creada: {folio} - Fecha: {fecha_dev}")

db.commit()
print(f"\n✅ {creadas} devoluciones de compra guardadas exitosamente")
print("\nAhora deberias ver datos en el reporte de devoluciones de compra para el rango 07/01/2026 - 10/02/2026")

db.close()
