#!/usr/bin/env python3
"""Script para verificar tokens JWT"""

from app.core.security import verify_token, create_access_token
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
    print(f"\n📝 Token generado:\n{test_token}\n")
    
    # Verificar el token
    payload = verify_token(test_token)
    if payload:
        print(f"✅ Token válido!")
        print(f"Payload: {payload}")
    else:
        print(f"❌ Token inválido")

db.close()
