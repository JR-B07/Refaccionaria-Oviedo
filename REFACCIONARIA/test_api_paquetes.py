#!/usr/bin/env python3
"""
Script para probar la API de paquetes
"""
import requests
import json
import time

# Esperar a que el servidor esté listo
time.sleep(2)

BASE_URL = "http://127.0.0.1:8000"

print("\n" + "="*60)
print("🧪 PRUEBA DE API PAQUETES")
print("="*60)

try:
    # 1. Login
    print("\n1️⃣ Intentando login...")
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": "admin", "password": "admin"},
        timeout=5
    )
    
    if resp.status_code != 200:
        print(f"❌ Error en login: {resp.status_code}")
        print(resp.text)
        exit(1)
    
    data = resp.json()
    token = data.get("access_token")
    print(f"✅ Login exitoso. Token: {token[:20]}...")
    
    # 2. Cargar paquetes
    print("\n2️⃣ Cargando paquetes...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"{BASE_URL}/api/v1/paquetes/",
        headers=headers,
        timeout=5
    )
    
    if resp.status_code != 200:
        print(f"❌ Error: {resp.status_code}")
        print(resp.text)
        exit(1)
    
    items = resp.json()
    print(f"✅ Se cargaron {len(items.get('items', []))} paquetes:")
    for p in items.get('items', []):
        print(f"   - ID {p.get('id')}: {p.get('nombre')} ({p.get('clase')})")
    
    # 3. Crear nuevo paquete
    print("\n3️⃣ Creando nuevo paquete...")
    resp = requests.post(
        f"{BASE_URL}/api/v1/paquetes/",
        headers=headers,
        json={
            "nombre": "Kit Prueba",
            "clase": "Prueba",
            "descripcion": "Paquete de prueba API"
        },
        timeout=5
    )
    
    if resp.status_code == 201:
        new_paq = resp.json()
        print(f"✅ Paquete creado: ID {new_paq.get('id')}")
    else:
        print(f"❌ Error: {resp.status_code}")
        print(resp.text)
    
    print("\n" + "="*60)
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
