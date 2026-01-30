#!/usr/bin/env python3
"""
Test para verificar que el login funciona correctamente
"""
import requests
import time
import json

time.sleep(2)

BASE_URL = "http://127.0.0.1:8000"

print("\n" + "="*60)
print("🧪 PRUEBA DE LOGIN Y PAQUETES")
print("="*60)

try:
    # 1. Login
    print("\n1️⃣ Intentando login...")
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": "admin", "password": "admin"},
        timeout=5
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    if resp.status_code != 200:
        print(f"❌ Error en login")
        exit(1)
    
    data = resp.json()
    token = data.get("access_token")
    print(f"✅ Login exitoso. Token: {token[:30]}...")
    
    # 2. Cargar paquetes
    print("\n2️⃣ Cargando paquetes con token...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"{BASE_URL}/api/v1/paquetes/",
        headers=headers,
        timeout=5
    )
    
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Response: {json.dumps(data, indent=2, default=str)}")
    
    if resp.status_code != 200:
        print(f"❌ Error: {resp.status_code}")
        exit(1)
    
    items = data.get('items', [])
    print(f"✅ Se cargaron {len(items)} paquetes:")
    for p in items:
        print(f"   - ID {p.get('id')}: {p.get('nombre')} ({p.get('clase')})")
    
    print("\n" + "="*60)
    print("✅ TODO FUNCIONA CORRECTAMENTE")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
