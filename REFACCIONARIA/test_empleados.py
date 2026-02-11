#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el endpoint de empleados
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "test_token"  # Reemplaza con un token válido si es necesario


def test_empleados():
    """Prueba los endpoints de empleados"""
    print("=" * 70)
    print("PRUEBAS DEL ENDPOINT DE EMPLEADOS")
    print("=" * 70)
    
    # 1. Obtener lista vacía
    print("\n1️⃣ GET /api/v1/empleados (listar)")
    response = requests.get(f"{BASE_URL}/empleados", headers={"Authorization": f"Bearer {TOKEN}"})
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 2. Crear un empleado
    print("\n2️⃣ POST /api/v1/empleados (crear)")
    empleado_data = {
        "nombre": "JUAN PÉREZ",
        "puesto": "VENDEDOR",
        "departamento": "VENTAS",
        "sucursal": "MATRIZ",
        "organizacion": "REFACCIONARIA OVIEDO",
        "fecha_alta": "2024-01-15",
        "activo": True,
        "notas": "Empleado activo"
    }
    response = requests.post(
        f"{BASE_URL}/empleados",
        json=empleado_data,
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        empleado_id = response.json()["id"]
        
        # 3. Obtener empleado por ID
        print(f"\n3️⃣ GET /api/v1/empleados/{empleado_id} (obtener por ID)")
        response = requests.get(
            f"{BASE_URL}/empleados/{empleado_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        print(f"Status: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 4. Actualizar empleado
        print(f"\n4️⃣ PUT /api/v1/empleados/{empleado_id} (actualizar)")
        update_data = {
            "puesto": "GERENTE VENTAS",
            "departamento": "VENTAS"
        }
        response = requests.put(
            f"{BASE_URL}/empleados/{empleado_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        print(f"Status: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 5. Listar con filtro
        print(f"\n5️⃣ GET /api/v1/empleados?nombre=JUAN (filtrar)")
        response = requests.get(
            f"{BASE_URL}/empleados?nombre=JUAN",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        print(f"Status: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    test_empleados()
