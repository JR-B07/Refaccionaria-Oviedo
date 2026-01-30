#!/usr/bin/env python3
import urllib.request
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

def test_post():
    print("\n=== POST /api/v1/asistencia/registrar ===")
    req = urllib.request.Request(
        f"{BASE_URL}/api/v1/asistencia/registrar",
        data=json.dumps({
            "nombre": "PRINCIPAL DE SISTEMA ADMINISTRADOR",
            "sucursal": "MATRIZ",
            "accion": "Entrada",
            "fecha": "2026-01-20",
            "hora": "08:00"
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Status: {resp.status}")
            data = json.loads(resp.read().decode())
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            return True
    except Exception as e:
        print(f"Error POST: {e}")
        return False

def test_get():
    print("\n=== GET /api/v1/asistencia ===")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/v1/asistencia") as resp:
            data = json.loads(resp.read().decode())
            print(f"Count: {data['count']}")
            print(f"Data ({len(data['data'])} registros):")
            for r in data["data"]:
                print(f"  - {r['nombre']} ({r['fecha']}): E={r['entrada']} C={r['comida']} R={r['regreso']} S={r['salida']}")
            return True
    except Exception as e:
        print(f"Error GET: {e}")
        return False

if __name__ == "__main__":
    print("Probando endpoints de asistencia...")
    test_post()
    test_get()
