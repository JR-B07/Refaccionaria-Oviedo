#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test endpoint de compras sin autenticación"""

import requests
import json

print("=" * 70)
print("TEST: GET /api/v1/compras (sin autenticación)")
print("=" * 70)

url = "http://localhost:8000/api/v1/compras"
params = {
    "fecha_inicio": "2026-01-01",
    "fecha_fin": "2026-02-28"
}

try:
    response = requests.get(url, params=params, timeout=5)
    print(f"\n✅ Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"✅ Respuesta: Lista con {len(data)} compras")
        if data:
            print(f"   Primera compra: {data[0].get('folio')} - {data[0].get('estado')}")
    else:
        print(f"❌ Error: {response.json()}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")
