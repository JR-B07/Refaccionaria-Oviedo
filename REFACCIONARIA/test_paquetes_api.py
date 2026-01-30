"""Script para probar el endpoint de paquetes"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Primero hacer login para obtener el token
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("=== Intentando hacer login ===")
try:
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"✓ Token obtenido: {token[:20]}...")
        
        # Probar el endpoint de paquetes
        print("\n=== Probando GET /api/v1/paquetes ===")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/paquetes", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Probar crear un paquete
        print("\n=== Probando POST /api/v1/paquetes ===")
        nuevo_paquete = {
            "nombre": "Paquete de Prueba",
            "descripcion": "Descripción de prueba",
            "clase": "Test"
        }
        response = requests.post(f"{BASE_URL}/api/v1/paquetes", json=nuevo_paquete, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    else:
        print(f"✗ Error en login: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
