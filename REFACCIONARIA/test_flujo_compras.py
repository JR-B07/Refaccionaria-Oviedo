#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para probar el flujo completo de compras"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8001/api/v1"

# 1. Obtener locales (sucursales)
print("\n1️⃣  Obteniendo locales...")
resp = requests.get(f"{BASE_URL}/locales")
locales = resp.json()
print(f"Locales encontrados: {len(locales)}")
for local in locales:
    print(f"   ID: {local['id']} - {local['nombre']}")

# 2. Obtener proveedores
print("\n2️⃣  Obteniendo proveedores...")
resp = requests.get(f"{BASE_URL}/proveedores")
proveedores = resp.json()
print(f"Proveedores encontrados: {len(proveedores)}")
for prov in proveedores:
    print(f"   ID: {prov['id']} - {prov['nombre']}")

# 3. Crear una compra
print("\n3️⃣  Creando compra...")
compra_data = {
    "folio": f"COMP-{date.today().isoformat()}",
    "fecha": date.today().isoformat(),
    "proveedor_id": 1,
    "local_id": 1,
    "estado": "pendiente",
    "subtotal": 1000.0,
    "descuento": 0.0,
    "iva": 160.0,
    "total": 1160.0,
    "tipo_moneda": "MXN",
    "notas": "Prueba desde script"
}

print(f"Enviando data: {json.dumps(compra_data, indent=2)}")
resp = requests.post(f"{BASE_URL}/compras", json=compra_data)
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")

# 4. Listar compras creadas
print("\n4️⃣  Listando compras...")
resp = requests.get(f"{BASE_URL}/compras")
compras = resp.json()
print(f"Total compras: {len(compras)}")
if compras:
    compra = compras[-1]
    print(f"Última compra:")
    print(f"   ID: {compra['id']}")
    print(f"   Folio: {compra['folio']}")
    print(f"   Total: {compra['total']}")
    print(f"   Estado: {compra['estado']}")
