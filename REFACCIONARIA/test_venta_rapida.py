#!/usr/bin/env python3
"""Script para probar el endpoint de venta rápida"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_venta_rapida():
    """Prueba el endpoint de venta rápida"""
    
    print("\n" + "="*80)
    print("PRUEBA DE VENTA RÁPIDA")
    print("="*80 + "\n")
    
    # Datos de prueba
    venta_data = {
        "folio": f"VZ{int(datetime.now().timestamp() % 10000)}",
        "local_id": 1,
        "usuario_id": 3,
        "cliente_id": None,
        "estado": "completada",  # minúsculas
        "tipo_venta": "contado",  # minúsculas
        "subtotal": 120.00,
        "descuento": 10.00,
        "iva": 17.60,
        "total": 127.60,
        "pago_recibido": 130.00,
        "cambio": 2.40,
        "metodo_pago": "efectivo",
        "fecha_limite_pago": None,
        "saldo_pendiente": 0.0
    }
    
    print(f"📤 Enviando datos a {BASE_URL}/ventas/rapida")
    print(f"\nDatos a enviar:")
    print(json.dumps(venta_data, indent=2, default=str))
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/ventas/rapida",
            json=venta_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"\nResponse:")
        
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2, default=str))
        except:
            print(response.text)
        
        if response.status_code == 200 or response.status_code == 201:
            print("\n✅ ¡ÉXITO! Venta registrada correctamente")
            return True
        else:
            print(f"\n❌ Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error al enviar la solicitud: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Verificar conexión primero
    print("Verificando conexión al servidor...")
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        print(f"✓ Servidor respondiendo: {response.status_code}\n")
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}\n")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:8000")
        exit(1)
    
    # Ejecutar prueba
    test_venta_rapida()
