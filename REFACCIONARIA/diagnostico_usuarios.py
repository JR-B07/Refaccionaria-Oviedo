#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para diagnosticar el problema con el endpoint"""

import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.usuario import Usuario, EstadoUsuario
from app.crud.usuario import usuario_crud

db = SessionLocal()

try:
    print("=" * 70)
    print("DIAGNÓSTICO DE USUARIOS")
    print("=" * 70)
    
    # Verificar usuarios en BD
    usuarios = db.query(Usuario).all()
    print(f"\n✅ Usuarios en la BD: {len(usuarios)}")
    
    for u in usuarios[:3]:
        print(f"\n  ID: {u.id}")
        print(f"  Nombre: {u.nombre}")
        print(f"  Nombre usuario: {u.nombre_usuario}")
        print(f"  Email: {u.email}")
        print(f"  Estado (type): {type(u.estado).__name__} = {u.estado!r}")
        print(f"  Estado value: {u.estado.value if hasattr(u.estado, 'value') else u.estado}")
    
    print("\n" + "-" * 70)
    print("PRUEBA: obtener_activos()")
    print("-" * 70)
    
    try:
        activos = usuario_crud.obtener_activos(db, skip=0, limit=100)
        print(f"✅ Usuarios acticos encontrados: {len(activos)}")
        for u in activos[:3]:
            print(f"  - {u.nombre_usuario}: {u.estado}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
except Exception as e:
    print(f"\n❌ Error de diagnóstico: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()

print("\n" + "=" * 70)
