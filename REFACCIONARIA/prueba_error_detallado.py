#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueba con detalles de error"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 70)
print("PRUEBA CON DETALLES DE ERROR")
print("=" * 70)

url = f"{BASE_URL}/usuarios/?skip=0&limit=100"
print(f"\n🔗 URL: {url}")
print("-" * 70)

try:
    response = requests.get(url, timeout=5)
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"\nHeaders:")
    for k, v in response.headers.items():
        print(f"  {k}: {v}")
    
    print(f"\nRespuesta:")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)

except Exception as e:
    print(f"\n❌ Error de conexión: {str(e)}")

print("\n" + "=" * 70)
