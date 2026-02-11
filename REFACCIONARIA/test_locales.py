#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar endpoint de locales"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 70)
print("PRUEBA DE ENDPOINT DE LOCALES")
print("=" * 70)

url = f"{BASE_URL}/locales"
print(f"\n🔗 URL: {url}")
print("-" * 70)

try:
    response = requests.get(url, timeout=5)
    print(f"\n✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Sucursales encontradas: {len(data)}")
        
        for i, local in enumerate(data, 1):
            print(f"\n{i}. {local.get('nombre', 'N/A')}")
            print(f"   ID: {local.get('id', 'N/A')}")
            print(f"   Dirección: {local.get('direccion', 'N/A')}")
    else:
        print(f"\n❌ Error: {response.text}")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 70)
