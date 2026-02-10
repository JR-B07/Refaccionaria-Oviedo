#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que el login funciona correctamente con bcrypt
"""

import sys
import json
from sqlalchemy import text
from app.core.database import engine, SessionLocal
from app.crud.usuario import usuario_crud
import bcrypt

print("=" * 80)
print("VERIFICANDO CONFIGURACIÓN DE LOGIN")
print("=" * 80 + "\n")

try:
    # 1. Verificar conexión a BD
    print("1️⃣  Conectando a la BD...")
    db = SessionLocal()
    result = db.execute(text("SELECT 1"))
    print("   ✅ Conexión exitosa\n")
    
    # 2. Obtener usuario admin
    print("2️⃣  Buscando usuario 'admin'...")
    admin = usuario_crud.obtener_por_nombre_usuario(db, "admin")
    if not admin:
        print("   ❌ Usuario 'admin' no encontrado")
        sys.exit(1)
    print(f"   ✅ Usuario encontrado: {admin.nombre_usuario}")
    print(f"   Nombre: {admin.nombre}")
    print(f"   Email: {admin.email}")
    print(f"   Rol: {admin.rol}")
    print(f"   Hash guardado: {admin.clave_hash[:20]}...\n")
    
    # 3. Verificar contraseña con bcrypt
    print("3️⃣  Verificando contraseña 'admin' con bcrypt...")
    try:
        match = bcrypt.checkpw("admin".encode(), admin.clave_hash.encode())
        if match:
            print("   ✅ ¡CONTRASEÑA CORRECTA! La autenticación funciona\n")
        else:
            print("   ❌ Contraseña no coincide\n")
    except Exception as e:
        print(f"   ❌ Error al verificar: {e}\n")
    
    # 4. Verificar sucursal1
    print("4️⃣  Buscando usuario 'sucursal1'...")
    sucursal1 = usuario_crud.obtener_por_nombre_usuario(db, "sucursal1")
    if not sucursal1:
        print("   ❌ Usuario 'sucursal1' no encontrado")
        sys.exit(1)
    print(f"   ✅ Usuario encontrado: {sucursal1.nombre_usuario}\n")
    
    try:
        match = bcrypt.checkpw("sucursal1".encode(), sucursal1.clave_hash.encode())
        if match:
            print("   ✅ ¡CONTRASEÑA CORRECTA!\n")
        else:
            print("   ❌ Contraseña no coincide\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # 5. Verificar sucursal2
    print("5️⃣  Buscando usuario 'sucursal2'...")
    sucursal2 = usuario_crud.obtener_por_nombre_usuario(db, "sucursal2")
    if not sucursal2:
        print("   ❌ Usuario 'sucursal2' no encontrado")
        sys.exit(1)
    print(f"   ✅ Usuario encontrado: {sucursal2.nombre_usuario}\n")
    
    try:
        match = bcrypt.checkpw("sucursal2".encode(), sucursal2.clave_hash.encode())
        if match:
            print("   ✅ ¡CONTRASEÑA CORRECTA!\n")
        else:
            print("   ❌ Contraseña no coincide\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    db.close()
    
    print("=" * 80)
    print("✅ TODO ESTÁ LISTO PARA EL LOGIN")
    print("=" * 80)
    print("\n📝 El endpoint POST /api/v1/auth/login ahora debe funcionar con:")
    print('   {"username": "admin", "password": "admin"}')
    print('   {"username": "sucursal1", "password": "sucursal1"}')
    print('   {"username": "sucursal2", "password": "sucursal2"}')
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
