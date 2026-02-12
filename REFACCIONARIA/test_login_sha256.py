#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para probar el login de todos los usuarios migrados a SHA256"""

import requests
import sys

BASE_URL = "http://localhost:8000"

# Usuarios migrados con sus contraseñas en SHA256
USUARIOS_PRUEBA = [
    {"username": "admin", "password": "admin", "nombre_esperado": "Administrador"},
    {"username": "sucursal1", "password": "sucursal1", "nombre_esperado": "Usuario Sucursal 1"},
    {"username": "sucursal2", "password": "sucursal2", "nombre_esperado": "Usuario Sucursal 2"},
]

print("=" * 80)
print("PRUEBA DE LOGIN CON SHA256 - TODOS LOS USUARIOS")
print("=" * 80)

# Verificar que el servidor esté corriendo
print("\n🔍 Verificando servidor...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("   ✅ Servidor activo")
    else:
        print(f"   ❌ Servidor respondió con código {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ No se puede conectar al servidor: {e}")
    print("   💡 Asegúrate de que el servidor esté corriendo con: python run.py")
    sys.exit(1)

# Probar cada usuario
print("\n🔐 Probando autenticación de usuarios...")
print("-" * 80)

exitosos = 0
fallidos = 0

for usuario in USUARIOS_PRUEBA:
    username = usuario["username"]
    password = usuario["password"]
    nombre_esperado = usuario.get("nombre_esperado", "")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"username": username, "password": password},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            nombre = data.get('user', {}).get('name', 'N/A')
            rol = data.get('user', {}).get('role', 'N/A')
            token_preview = data.get('access_token', '')[:40]
            
            print(f"✅ {username:12} | Login exitoso")
            print(f"   👤 Nombre: {nombre}")
            print(f"   🎭 Rol: {rol}")
            print(f"   🔑 Token: {token_preview}...")
            exitosos += 1
        else:
            print(f"❌ {username:12} | Login falló")
            print(f"   📄 Respuesta: {response.text[:100]}")
            fallidos += 1
            
    except Exception as e:
        print(f"❌ {username:12} | Error: {e}")
        fallidos += 1
    
    print("-" * 80)

# Resumen
print("\n📊 RESUMEN DE PRUEBAS")
print("=" * 80)
print(f"✅ Exitosos: {exitosos}")
print(f"❌ Fallidos: {fallidos}")
print(f"📈 Total: {exitosos + fallidos}")

if fallidos == 0:
    print("\n🎉 ¡Todos los usuarios pudieron iniciar sesión correctamente!")
    print("✅ La migración a SHA256 fue exitosa")
else:
    print(f"\n⚠️  {fallidos} usuario(s) tuvieron problemas al iniciar sesión")
    print("💡 Verifica que las contraseñas se hayan migrado correctamente")

print("=" * 80)

# Información adicional
print("\n📝 INFORMACIÓN DE CONTRASEÑAS SHA256")
print("-" * 80)
print("Usuario    | Contraseña  | Hash SHA256")
print("-" * 80)

import hashlib
for usuario in USUARIOS_PRUEBA:
    username = usuario["username"]
    password = usuario["password"]
    hash_sha256 = hashlib.sha256(password.encode()).hexdigest()
    print(f"{username:10} | {password:11} | {hash_sha256}")

print("-" * 80)
