#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para simular el endpoint de usuarios"""

import sys
sys.path.insert(0, '.')
import json
from app.core.database import SessionLocal
from app.crud.usuario import usuario_crud
from app.schemas.usuario import UsuarioResponse

db = SessionLocal()

try:
    print("=" * 70)
    print("SIMULACIÓN DE ENDPOINT /usuarios/")
    print("=" * 70)
    
    # Obtener usuarios (como hace el endpoint)
    usuarios = usuario_crud.obtener_activos(db, skip=0, limit=100)
    print(f"\n✅ Usuarios obtenidos: {len(usuarios)}")
    
    print("\n" + "-" * 70)
    print("CONVERSIÓN A UsuarioResponse (Pydantic)")
    print("-" * 70)
    
    # Intentar convertir a UsuarioResponse
    usuarios_response = []
    for u in usuarios:
        try:
            response =UsuarioResponse.model_validate(u)
            usuarios_response.append(response)
            print(f"\n✅ {u.nombre_usuario}:")
            print(f"   ID: {response.id}")
            print(f"   Email: {response.email}")
            print(f"   Estado: {response.estado}")
            print(f"   Rol: {response.rol}")
        except Exception as e:
            print(f"\n❌ Error al convertir {u.nombre_usuario}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "-" * 70)
    print("SERIALIZACIÓN A JSON")
    print("-" * 70)
    
    # Intentar serializar a JSON
    try:
        json_data = json.dumps([u.model_dump() for u in usuarios_response], indent=2, default=str)
        print(f"\n✅ Serialización exitosa ({len(json_data)} caracteres)")
        print(f"\nPrimeros 500 caracteres:")
        print(json_data[:500])
    except Exception as e:
        print(f"\n❌ Error en serialización: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"\n❌ Error general: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()

print("\n" + "=" * 70)
