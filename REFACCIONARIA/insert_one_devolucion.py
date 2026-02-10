from app.core.database import SessionLocal
from app.models.venta import Venta, DetalleVenta
from datetime import datetime

db = SessionLocal()

# Datos de prueba
cliente_id = 7  # CLIENTE PRUEBA
usuario_id = 3  # Admin
local_id = 1
fecha_crear = datetime(2026, 1, 15)

# Crear una simple venta devuelta
try:
    venta = Venta(
        folio=f"VTA-2026DEV{hash('test') % 10000:04d}",  # Generar folio único
        local_id=local_id,
        usuario_id=usuario_id,
        cliente_id=cliente_id,
        tipo_venta="contado",
        estado="devuelta",
        subtotal=500.00,
        descuento=0.00,
        iva=125.00,
        total=625.00,
        pago_recibido=625.00,
        cambio=0.00,
        metodo_pago="EFECTIVO",
        fecha_creacion=fecha_crear
    )
    
    db.add(venta)
    db.commit()
    db.refresh(venta)
    
    # Agregar detalle
    detalle = DetalleVenta(
        venta_id=venta.id,
        producto_id=1,
        local_id=local_id,  # Agregar local_id
        cantidad=5,
        precio_unitario=125.00,
        importe=625.00
    )
    db.add(detalle)
    db.commit()
    
    print(f"✅ Venta devuelta creada: {venta.folio} - Total: $625.00")
    
    # Verificar
    count = db.query(Venta).filter(Venta.estado == "devuelta").count()
    print(f"✅ Total de ventas devueltas en BD: {count}")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
