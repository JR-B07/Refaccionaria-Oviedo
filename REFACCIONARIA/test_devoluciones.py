#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para probar el endpoint de devoluciones detalladas"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 70)
print("PRUEBA DE ENDPOINT DE DEVOLUCIONES DETALLADAS")
print("=" * 70)

# Fechas de prueba (amplio rango para incluir datos históricos)
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=2555)  # Aproximadamente 7 años atrás

fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")

print(f"\n📅 Rango de fechas: {fecha_inicio_str} a {fecha_fin_str}")
print("-" * 70)

# Construir URL
url = f"{BASE_URL}/reportes/devoluciones-detalladas"
params = {
    "fecha_inicio": fecha_inicio_str,
    "fecha_fin": fecha_fin_str
}

print(f"\n🔗 URL: {url}")
print(f"📊 Parámetros: {json.dumps(params, indent=2)}")
print("-" * 70)

try:
    print("\n⏳ Realizando solicitud al endpoint...")
    response = requests.get(url, params=params, timeout=10)
    
    print(f"\n✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n📈 Resultados del reporte:")
        print(f"  • Total de devoluciones: {data.get('total', 0)}")
        print(f"  • Monto total: ${data.get('total_monto', 0):,.2f}")
        
        devoluciones = data.get('devoluciones', [])
        
        if devoluciones:
            print(f"\n📋 Primeras 5 devoluciones:")
            for i, dev in enumerate(devoluciones[:5], 1):
                print(f"\n  {i}. Folio: {dev.get('folio', 'N/A')}")
                print(f"     Fecha venta: {dev.get('fecha_venta', 'N/A')}")
                print(f"     Fecha devolución: {dev.get('fecha_devolucion', 'N/A')}")
                print(f"     Sucursal: {dev.get('sucursal', 'N/A')}")
                print(f"     Vendedor: {dev.get('vendedor', 'N/A')}")
                print(f"     Producto: {dev.get('producto', 'N/A')}")
                print(f"     Monto: ${float(dev.get('monto', 0)):,.2f}")
        else:
            print("\n⚠️  No se encontraron devoluciones en el rango de fechas especificado")
            print("    Esto puede ser normal si no hay ventas con estado 'devuelta'")
            
    else:
        print(f"\n❌ Error en la respuesta:")
        try:
            error_data = response.json()
            print(f"   {json.dumps(error_data, indent=2)}")
        except:
            print(f"   {response.text}")

except requests.exceptions.Timeout:
    print("\n❌ Error: Timeout - El servidor no respondió a tiempo")
except requests.exceptions.ConnectionError:
    print("\n❌ Error: No se pudo conectar al servidor")
    print("   Asegúrate de que el servidor esté corriendo en http://localhost:8001")
except Exception as e:
    print(f"\n❌ Error inesperado: {str(e)}")

print("\n" + "=" * 70)
print("FIN DE PRUEBAS")
print("=" * 70)
