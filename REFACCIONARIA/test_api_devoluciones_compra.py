#!/usr/bin/env python
"""
Script de prueba para verificar el endpoint de API de devoluciones_compra
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Test 1: Listar devoluciones (GET)
print("=" * 60)
print("TEST 1: Listar devoluciones")
print("=" * 60)

response = requests.get(f"{BASE_URL}/api/v1/devoluciones-compra")
print(f"Status: {response.status_code}")
print(f"Respuesta: {json.dumps(response.json(), indent=2, default=str)[:500]}...")
print()

# Test 2: Crear una devolución (POST)
print("=" * 60)
print("TEST 2: Crear una devolución")
print("=" * 60)

nueva_devolucion = {
    "folio": "DEV-TEST-001",
    "factura": "F-TEST-123",
    "proveedor_id": 1,
    "estado": "pendiente",
    "fecha_devolucion": "2026-02-09",
    "nota_credito": "NC-TEST-001",
    "producto_nombre": "PRODUCTO TEST",
    "cantidad": 1,
    "precio_unitario": 100.0,
    "monto_total": 100.0,
    "descripcion": "Prueba de API",
    "local_id": 1,
    "usuario_id": 1
}

response = requests.post(
    f"{BASE_URL}/api/v1/devoluciones-compra",
    json=nueva_devolucion
)
print(f"Status: {response.status_code}")
print(f"Respuesta: {json.dumps(response.json(), indent=2, default=str)}")
print()

# Guardar ID para pruebas posteriores
if response.status_code == 200:
    devolucion_id = response.json().get('id')
    print(f"✓ Devolución creada con ID: {devolucion_id}")
    
    # Test 3: Obtener una devolución por ID (GET)
    print()
    print("=" * 60)
    print(f"TEST 3: Obtener devolución {devolucion_id}")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/v1/devoluciones-compra/{devolucion_id}")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, default=str)}")
    print()
    
    # Test 4: Actualizar la devolución (PUT)
    print("=" * 60)
    print(f"TEST 4: Actualizar devolución {devolucion_id}")
    print("=" * 60)
    
    actualizar = {
        "estado": "aprobada",
        "nota_credito": "NC-TEST-002"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/v1/devoluciones-compra/{devolucion_id}",
        json=actualizar
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, default=str)}")
    print()
    
    # Test 5: Eliminar la devolución (DELETE)
    print("=" * 60)
    print(f"TEST 5: Eliminar devolución {devolucion_id}")
    print("=" * 60)
    
    response = requests.delete(f"{BASE_URL}/api/v1/devoluciones-compra/{devolucion_id}")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, default=str)}")
    print()
    
    print("✓ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
else:
    print(f"✗ Error al crear devolución: {response.status_code}")
    print(f"Respuesta: {response.json()}")
