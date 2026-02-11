#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para probar el endpoint de estadísticas de ventas"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 70)
print("PRUEBA DE ENDPOINT DE ESTADÍSTICAS DE VENTAS")
print("=" * 70)

# Obtener año actual
año_actual = datetime.now().year
mes_actual = datetime.now().month

urls = [
    (f"{BASE_URL}/reportes/estadisticas-ventas?tipo=anual&anio={año_actual}", "Datos anuales"),
    (f"{BASE_URL}/reportes/estadisticas-ventas?tipo=mensual&anio={año_actual}", "Datos mensuales"),
    (f"{BASE_URL}/reportes/estadisticas-ventas?tipo=diaria&anio={año_actual}&mes={mes_actual}", "Datos diarios"),
]

for url, desc in urls:
    print(f"\n{desc}")
    print(f"URL: {url}")
    print("-" * 70)
    
    try:
        resp = requests.get(url, timeout=5)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Datos recibidos:")
            print(f"  - Labels: {data.get('labels', [])[:5]}...")
            print(f"  - Ventas: {data.get('ventas', [])[:5]}...")
            print(f"  - Cantidad: {data.get('cantidad', [])[:5]}...")
            print(f"  - Total ventas: ${sum(data.get('ventas', []))}")
            print(f"  - Total registros: {sum(data.get('cantidad', []))}")
        else:
            print(f"❌ Error: {resp.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

print("\n" + "=" * 70)
print("FIN DE PRUEBAS")
print("=" * 70)
