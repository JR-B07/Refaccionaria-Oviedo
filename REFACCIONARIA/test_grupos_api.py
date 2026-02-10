#!/usr/bin/env python3
"""
Script de prueba para el endpoint de grupos de la API.
Prueba además los endpoints de productos por grupo.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_get_grupos():
    """Prueba obtener la lista de grupos"""
    print("=" * 60)
    print("PRUEBA 1: GET /api/v1/grupos/")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/grupos/")
        print(f"Status Code: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print(f"✓ Respuesta exitosa:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if 'items' in data:
                print(f"\n✓ Se encontraron {len(data.get('items', []))} grupos")
                return data.get('items', [])
            else:
                print("⚠️ La respuesta no contiene 'items'")
                return []
        else:
            print(f"✗ Error {response.status_code}:")
            print(response.text)
            return []
    except requests.exceptions.ConnectionError:
        print("✗ Error de conexión. ¿Está ejecutándose el servidor en localhost:8000?")
        return []
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def test_get_productos_grupo(grupo_id):
    """Prueba obtener productos de un grupo"""
    print("\n" + "=" * 60)
    print(f"PRUEBA: GET /api/v1/grupos/{grupo_id}/productos")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/grupos/{grupo_id}/productos")
        print(f"Status Code: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print(f"✓ Respuesta exitosa:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])  # Primeros 500 chars
            return True
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    grupos = test_get_grupos()
    
    if grupos:
        print("\n" + "=" * 60)
        print("Probando endpoints de productos para cada grupo")
        print("=" * 60)
        for grupo in grupos:
            test_get_productos_grupo(grupo['id'])

