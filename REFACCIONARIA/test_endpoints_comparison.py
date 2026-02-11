#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar endpoints GET /
"""

import requests

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "test_token"

endpoints = [
    "/usuarios",
    "/empleados",
    "/usuarios/",
    "/empleados/",
]

print("=" * 70)
print("COMPARACIÓN DE ENDPOINTS GET /")
print("=" * 70)

for endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    print(f"\n[TEST] GET {url}")
    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Retorna lista con {len(data)} items")
            else:
                print(f"✅ Response: {str(data)[:100]}")
        else:
            print(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
