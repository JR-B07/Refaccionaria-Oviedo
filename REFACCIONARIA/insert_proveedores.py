from app.core.database import SessionLocal
from app.models.proveedor import Proveedor

db = SessionLocal()

proveedores = [
    {
        'clave': 'PROV001',
        'nombre': 'AUTOPARTES DEL NORTE S.A. DE C.V.',
        'rfc': 'ADN850623G45',
        'contacto_compras_telefono': '8181234567',
        'contacto_compras_email': 'ventas@autopartesnorte.com.mx',
        'calle': 'Av. Industria',
        'numero_exterior': '123',
        'ciudad': 'Monterrey',
        'estado': 'Nuevo León',
        'codigo_postal': '64000',
        'dias_entrega': 5,
        'descuento_factura': 5.0
    },
    {
        'clave': 'PROV002',
        'nombre': 'REFACCIONES GARCIA Y ASOCIADOS S.C.',
        'rfc': 'RGA920415H78',
        'contacto_compras_telefono': '3338765432',
        'contacto_compras_email': 'pedidos@refaccionesgarcia.com',
        'calle': 'Blvd. Tlaquepaque',
        'numero_exterior': '456',
        'ciudad': 'Guadalajara',
        'estado': 'Jalisco',
        'codigo_postal': '44100',
        'dias_entrega': 3,
        'descuento_factura': 3.0
    },
    {
        'clave': 'PROV003',
        'nombre': 'LUBRICANTES SUPREMOS DE MEXICO S.A.',
        'rfc': 'LSM880307K21',
        'contacto_compras_telefono': '5555123456',
        'contacto_compras_email': 'contacto@lubricantesupremos.mx',
        'calle': 'Calz. de Tlalpan',
        'numero_exterior': '789',
        'ciudad': 'Ciudad de México',
        'estado': 'CDMX',
        'codigo_postal': '03100',
        'dias_entrega': 7,
        'descuento_factura': 8.0
    },
    {
        'clave': 'PROV004',
        'nombre': 'DISTRIBUIDORA DE FILTROS PREMIUM S.A.',
        'rfc': 'DFP900512M34',
        'contacto_compras_telefono': '4424567890',
        'contacto_compras_email': 'info@filtrospremium.com.mx',
        'calle': 'Av. Constitución',
        'numero_exterior': '321',
        'ciudad': 'Querétaro',
        'estado': 'Querétaro',
        'codigo_postal': '76000',
        'dias_entrega': 4,
        'descuento_factura': 4.5
    },
    {
        'clave': 'PROV005',
        'nombre': 'FRENOS INDUSTRIALES DE OCCIDENTE S.A.',
        'rfc': 'FIO931128N56',
        'contacto_compras_telefono': '3337654321',
        'contacto_compras_email': 'ventas@frenosindustriales.com',
        'calle': 'Carr. a Zapopan',
        'numero_exterior': '654',
        'ciudad': 'Guadalajara',
        'estado': 'Jalisco',
        'codigo_postal': '44500',
        'dias_entrega': 5,
        'descuento_factura': 6.0
    }
]

try:
    for prov_data in proveedores:
        proveedor = Proveedor(**prov_data)
        db.add(proveedor)
    
    db.commit()
    print('✅ 5 proveedores insertados correctamente')
except Exception as e:
    db.rollback()
    print(f'❌ Error: {e}')
finally:
    db.close()
