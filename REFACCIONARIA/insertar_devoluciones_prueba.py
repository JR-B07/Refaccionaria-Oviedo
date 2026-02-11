from app.core.database import SessionLocal
from app.models.venta import Venta, DetalleVenta
from app.models.cliente import Cliente
from datetime import datetime, timedelta

db = SessionLocal()

# Crear cliente de prueba si no existe
cliente_prueba = db.query(Cliente).filter(Cliente.nombre == "CLIENTE PRUEBA").first()
if not cliente_prueba:
    cliente_prueba = Cliente(
        nombre="CLIENTE PRUEBA",
        apellido_paterno="TEST",
        apellido_materno="TEST",
        email="prueba@test.com",
        telefono="123456789",
        tipo_figura="Persona Física"
    )
    db.add(cliente_prueba)
    db.commit()
    print(f"✅ Cliente de prueba creado: {cliente_prueba.id}")
else:
    print(f"✅ Cliente de prueba ya existe: {cliente_prueba.id}")

# Insertar 3 ventas devueltas en el rango Jul-Oct 2026
ventas_prueba = []
fechas = [
    datetime(2026, 7, 5),
    datetime(2026, 8, 10),
    datetime(2026, 9, 20),
]

folio_base = 8000
for i, fecha in enumerate(fechas):
    folio = f"VTA-2026020{folio_base + i}"
    
    venta = Venta(
        folio=folio,
        local_id=1,
        usuario_id=3,  # ID del usuario admin
        cliente_id=cliente_prueba.id,
        tipo_venta="contado",  # contado, credito, apartado
        estado="devuelta",
        subtotal=500.00,
        descuento=0.00,
        iva=125.00,
        total=625.00,
        pago_recibido=625.00,
        cambio=0.00,
        metodo_pago="EFECTIVO",
        fecha_creacion=fecha
    )
    
    db.add(venta)
    db.flush()  # Para obtener el ID antes de commit
    
    # Agregar detalles de venta
    detalle = DetalleVenta(
        venta_id=venta.id,
        producto_id=1,
        local_id=1,
        cantidad=5,
        precio_unitario=125.00,
        importe=625.00
    )
    db.add(detalle)
    ventas_prueba.append(venta)
    
    print(f"✅ Venta devuelta creada: {folio} - Fecha: {fecha.strftime('%Y-%m-%d')} - Total: $625.00")

db.commit()
print(f"\n✅ {len(ventas_prueba)} ventas devueltas de prueba guardadas exitosamente")
print("\nAhora deberías ver datos en el reporte para el rango 07/01/2026 - 10/02/2026")

db.close()
