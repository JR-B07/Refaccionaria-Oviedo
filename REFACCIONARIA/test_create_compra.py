#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test crear compra"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 70)
print("TEST: POST /api/v1/compras")
print("=" * 70)

compra_data = {
    "folio": "COMP-TEST-001",
    "factura": "F-2026-001",
    "fecha": str(date.today()),  # "2026-02-09"
    "proveedor_id": 1,  # Usar un proveedor que exista
    "local_id": 1,
    "estado": "completo",
    "subtotal": 1000.0,
    "descuento": 100.0,
    "iva": 144.0,
    "total": 1044.0,
    "tipo_moneda": "pesos",
    "notas": "Compra de prueba"
}

print(f"\nEnviando datos:")
print(json.dumps(compra_data, indent=2, ensure_ascii=False))

try:
    response = requests.post(BASE_URL + "/compras", json=compra_data, timeout=5)
    print(f"\n✅ Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"✅ Compra creada exitosamente")
        print(f"   ID: {data.get('id')}")
        print(f"   Folio: {data.get('folio')}")
        print(f"   Total: ${data.get('total')}")
    else:
        print(f"❌ Error {response.status_code}")
        print(f"   Details: {response.json()}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")
