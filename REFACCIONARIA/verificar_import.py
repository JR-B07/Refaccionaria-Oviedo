#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar importación del endpoint"""

import sys
sys.path.insert(0, '.')

print("=" * 70)
print("VERIFICACIÓN DE IMPORTACIÓN")
print("=" * 70)

try:
    print("\n1. Importando app.schemas.usuario...")
    from app.schemas.usuario import UsuarioResponse
    print(f"   ✅ UsuarioResponse importado: {UsuarioResponse}")
    
    print("\n2. Importando app.api.v1.endpoints.usuarios...")
    from app.api.v1.endpoints import usuarios as usuarios_module
    print(f"   ✅ Router: {usuarios_module.router}")
    
    print("\n3. Verificando funciones del router...")
    for route in usuarios_module.router.routes:
        print(f"   - {route.path} [{route.methods}]")
    
    print("\n✅ Todas las importaciones exitosas")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
