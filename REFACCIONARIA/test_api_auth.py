#!/usr/bin/env python3
"""Script para probar autenticación de API"""

import requests
from app.core.security import create_access_token
from app.core.database import SessionLocal
from app.crud.usuario import usuario_crud

# Conectar a base de datos
db = SessionLocal()

# Obtener el usuario admin
admin = usuario_crud.obtener_por_nombre_usuario(db, "admin")

if not admin:
    print("❌ No se encontró usuario admin")
else:
    print(f"✅ Usuario encontrado: {admin.nombre_usuario}")
    
    # Crear un token test
    token_data = {
        "sub": admin.nombre_usuario,
        "id": admin.id,
        "role": admin.rol.value if admin.rol else "vendedor",
        "local_id": admin.local_id,
    }
    
    test_token = create_access_token(token_data)
    print(f"\n📝 Token generado para pruebas de API\n")
    
    # Probar endpoint de compras
    url = "http://localhost:8000/api/v1/compras"
    headers = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json"
    }
    
    print(f"🌐 Probando GET {url}")
    print(f"📋 Headers: {headers}")
    
    response = requests.get(url, headers=headers)
    
    print(f"\n📊 Respuesta:")
    print(f"   Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"   ✅ Éxito! Recepciones encontradas: {len(data)}")
        for r in data[:3]:  # Mostrar primeras 3
            print(f"      - {r['folio']}: ${r['total']}")
    else:
        print(f"   ❌ Error: {response.text}")

db.close()
