#!/usr/bin/env python3
"""Script de prueba para los endpoints de tickets/vales"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def prueba_crear_vale():
    print("\n" + "="*60)
    print("1️⃣  PRUEBA: Crear un nuevo vale")
    print("="*60)
    
    datos = {
        "folio": "VZ20260201-TEST",
        "cliente": "Cliente Prueba",
        "articulo": "Producto Prueba",
        "partidas": 5,
        "estatus": "Pendiente",
        "fecha": datetime.now().date().isoformat()
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tickets/", json=datos)
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            resultado = response.json()
            print("✅ Vale creado exitosamente:")
            print(json.dumps(resultado, indent=2, default=str))
            return resultado.get("folio")
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def prueba_listar_vales():
    print("\n" + "="*60)
    print("2️⃣  PRUEBA: Listar todos los vales")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/tickets/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            vales = response.json()
            print(f"✅ Se encontraron {len(vales)} vales:")
            for vale in vales:
                print(f"  - {vale['folio']}: {vale['cliente']} ({vale['estatus']})")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def prueba_obtener_vale(folio):
    print("\n" + "="*60)
    print(f"3️⃣  PRUEBA: Obtener vale {folio}")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/tickets/{folio}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            vale = response.json()
            print("✅ Vale encontrado:")
            print(json.dumps(vale, indent=2, default=str))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def prueba_editar_vale(folio):
    print("\n" + "="*60)
    print(f"4️⃣  PRUEBA: Editar vale {folio}")
    print("="*60)
    
    datos = {
        "folio": folio,
        "cliente": "Cliente Actualizado",
        "articulo": "Producto Actualizado",
        "partidas": 10,
        "estatus": "Parcial",
        "fecha": datetime.now().date().isoformat()
    }
    
    try:
        response = requests.put(f"{BASE_URL}/tickets/{folio}", json=datos)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resultado = response.json()
            print("✅ Vale actualizado exitosamente:")
            print(json.dumps(resultado, indent=2, default=str))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def prueba_marcar_entregado(folio):
    print("\n" + "="*60)
    print(f"5️⃣  PRUEBA: Marcar vale {folio} como entregado")
    print("="*60)
    
    try:
        response = requests.post(f"{BASE_URL}/tickets/{folio}/entregar")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resultado = response.json()
            print("✅ Vale marcado como entregado:")
            print(json.dumps(resultado, indent=2, default=str))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def prueba_eliminar_vale(folio):
    print("\n" + "="*60)
    print(f"6️⃣  PRUEBA: Eliminar vale {folio}")
    print("="*60)
    
    try:
        response = requests.delete(f"{BASE_URL}/tickets/{folio}")
        print(f"Status: {response.status_code}")
        if response.status_code == 204:
            print(f"✅ Vale {folio} eliminado exitosamente")
        elif response.status_code == 200:
            print(f"✅ Vale eliminado (respuesta vacía)")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("\n" + "🧪 INICIANDO PRUEBAS DE ENDPOINTS DE TICKETS" + "\n")
    
    # Listar vales existentes
    prueba_listar_vales()
    
    # Crear un nuevo vale
    folio_creado = prueba_crear_vale()
    
    if folio_creado:
        # Obtener el vale creado
        prueba_obtener_vale(folio_creado)
        
        # Editar el vale
        prueba_editar_vale(folio_creado)
        
        # Marcar como entregado
        prueba_marcar_entregado(folio_creado)
        
        # Eliminar el vale
        prueba_eliminar_vale(folio_creado)
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60 + "\n")
