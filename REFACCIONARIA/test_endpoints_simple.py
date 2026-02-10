#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para probar endpoints GET /
"""

import requests
import sys

# Suprimir logs de SQLAlchemy
import logging
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)

BASE_URL = "http://localhost:8000/api/v1"

endpoints = [
    "/usuarios",
    "/empleados",
    "/usuarios/",
    "/empleados/",
]

print("=" * 70)
print("COMPARACIÓN DE ENDPOINTS GET")
print("=" * 70)

for endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    print(f"\n[TEST] GET {endpoint}")
    try:
        response = requests.get(url, timeout=5)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"  Data: ✅ Lista con {len(data)} items")
            else:
                print(f"  Data: OK")
        else:
            try:
                print(f"  Error: {response.json().get('detail', 'Unknown')}")
            except:
                print(f"  Error: {response.text[:100]}")
    except Exception as e:
        print(f"  Exception: {str(e)}")
