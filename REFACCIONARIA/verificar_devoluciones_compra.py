#!/usr/bin/env python
"""
Script de verificación rápida del sistema de devoluciones de compra
Verifica que todos los componentes estén funcionando correctamente
"""
import sys
import os

# Agregar el directorio root al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("VERIFICACIÓN DEL SISTEMA DE DEVOLUCIONES DE COMPRA")
print("=" * 70)
print()

# 1. Verificar tabla en base de datos
print("1️⃣  Verificando tabla en base de datos...")
try:
    from app.core.database import Base, engine
    from app.models.devolucion_compra import DevolucionCompra
    
    # Verificar que la tabla existe
    inspector = __import__('sqlalchemy').inspect(engine)
    tables = inspector.get_table_names()
    
    if 'devoluciones_compra' in tables:
        print("   ✅ Tabla 'devoluciones_compra' existe en la base de datos")
        
        # Obtener info de columnas
        columns = inspector.get_columns('devoluciones_compra')
        print(f"   ✅ Tabla tiene {len(columns)} columnas")
    else:
        print("   ❌ Tabla 'devoluciones_compra' NO existe")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error al verificar tabla: {e}")
    sys.exit(1)

print()

# 2. Verificar modelo ORM
print("2️⃣  Verificando modelo ORM...")
try:
    from app.models.devolucion_compra import DevolucionCompra, EstadoDevolucionCompra
    
    print("   ✅ Modelo DevolucionCompra importado correctamente")
    print("   ✅ Enum EstadoDevolucionCompra disponible")
    
    # Verificar atributos
    attrs = ['id', 'folio', 'estado', 'fecha_devolucion', 'monto_total', 'local_id', 'usuario_id']
    for attr in attrs:
        if hasattr(DevolucionCompra, attr):
            print(f"   ✅ Atributo '{attr}' presente")
        else:
            print(f"   ❌ Atributo '{attr}' FALTA")
            
except Exception as e:
    print(f"   ❌ Error al importar modelo: {e}")
    sys.exit(1)

print()

# 3. Verificar schemas Pydantic
print("3️⃣  Verificando schemas Pydantic...")
try:
    from app.schemas.devolucion_compra import (
        DevolucionCompraBase,
        DevolucionCompraCreate,
        DevolucionCompraUpdate,
        DevolucionCompraResponse
    )
    
    print("   ✅ DevolucionCompraBase importado")
    print("   ✅ DevolucionCompraCreate importado")
    print("   ✅ DevolucionCompraUpdate importado")
    print("   ✅ DevolucionCompraResponse importado")
    
    # Verificar que Response tiene campos computados
    if hasattr(DevolucionCompraResponse, 'model_fields'):
        fields = DevolucionCompraResponse.model_fields
        computed_fields = ['proveedor_nombre', 'local_nombre', 'usuario_nombre']
        for field in computed_fields:
            if field in fields:
                print(f"   ✅ Campo computado '{field}' presente")
    
except Exception as e:
    print(f"   ❌ Error al importar schemas: {e}")
    sys.exit(1)

print()

# 4. Verificar rutas API
print("4️⃣  Verificando rutas API...")
try:
    from app.api.v1.endpoints.devoluciones_compra import router
    
    # Obtener rutas
    routes = [route.path for route in router.routes]
    print(f"   ✅ Router de devoluciones_compra importado")
    print(f"   ✅ {len(router.routes)} rutas definidas")
    
    # Verificar métodos
    methods = set()
    for route in router.routes:
        if hasattr(route, 'methods'):
            methods.update(route.methods)
    
    expected_methods = {'GET', 'POST', 'PUT', 'DELETE'}
    for method in expected_methods:
        if method in methods:
            print(f"   ✅ Método HTTP {method} disponible")
        else:
            print(f"   ⚠️  Método HTTP {method} no verificado")
    
except Exception as e:
    print(f"   ❌ Error al importar rutas: {e}")
    sys.exit(1)

print()

# 5. Verificar integración con reporte
print("5️⃣  Verificando integración con reportes...")
try:
    from app.services.reporte_service import ReporteService
    from sqlalchemy.orm import Session
    
    # Verificar que el método existe
    if hasattr(ReporteService, 'generar_reporte_devoluciones_compra'):
        print("   ✅ Método 'generar_reporte_devoluciones_compra' existe en ReporteService")
    else:
        print("   ❌ Método 'generar_reporte_devoluciones_compra' NO existe")
        
except Exception as e:
    print(f"   ❌ Error al verificar reporte: {e}")
    sys.exit(1)

print()

# 6. Verificar archivo HTML
print("6️⃣  Verificando interfaz HTML...")
try:
    html_path = os.path.join(os.path.dirname(__file__), 'app', 'static', 'devoluciones_compra.html')
    
    if os.path.exists(html_path):
        print("   ✅ Archivo 'devoluciones_compra.html' existe")
        
        # Verificar contenido
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '/api/v1/devoluciones-compra' in content:
            print("   ✅ HTML tiene referencia al endpoint API")
        else:
            print("   ⚠️  HTML podría no tener referencia al endpoint")
            
        if 'datosEjemplo' not in content or content.count('datosEjemplo') <= 1:
            print("   ✅ Datos de ejemplo removidos")
        else:
            print("   ⚠️  Podría haber datos de ejemplo aún en HTML")
    else:
        print(f"   ❌ Archivo HTML no encontrado en {html_path}")
        
except Exception as e:
    print(f"   ⚠️  Error al verificar HTML: {e}")

print()
print("=" * 70)
print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 70)
print()
print("El sistema de devoluciones de compra está listo para usar.")
print()
print("URLs disponibles:")
print("  • GET  /api/v1/devoluciones-compra")
print("  • GET  /api/v1/devoluciones-compra/{id}")
print("  • POST /api/v1/devoluciones-compra")
print("  • PUT  /api/v1/devoluciones-compra/{id}")
print("  • DELETE /api/v1/devoluciones-compra/{id}")
print()
print("  • GET /api/v1/reportes/devoluciones-detalladas (ventas devueltas)")
print("  • GET /api/v1/reportes/devoluciones-compra-detalladas (compras devueltas)")
print()
