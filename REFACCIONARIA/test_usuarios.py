#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar el endpoint de usuarios"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 70)
print("PRUEBA DE ENDPOINT DE USUARIOS")
print("=" * 70)

url = f"{BASE_URL}/usuarios/?skip=0&limit=100"
print(f"\n🔗 URL: {url}")
print("-" * 70)

try:
    response = requests.get(url, timeout=5)
    print(f"\n✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Usuarios encontrados: {len(data)}")
        
        for i, usuario in enumerate(data[:5], 1):  # Mostrar primeros 5
            print(f"\n{i}. Nombre: {usuario.get('nombre', 'N/A')}")
            print(f"   Nombre usuario: {usuario.get('nombre_usuario', 'N/A')}")
            print(f"   Nombre completo: {usuario.get('nombre_completo', 'N/A')}")
            print(f"   Email: {usuario.get('email', 'N/A')}")
            print(f"   ID: {usuario.get('id', 'N/A')}")
            print(f"   Rol: {usuario.get('rol', 'N/A')}")
    else:
        print(f"\n❌ Error: {response.text}")

except Exception as e:
    print(f"\n❌ Error de conexión: {str(e)}")

print("\n" + "=" * 70)
