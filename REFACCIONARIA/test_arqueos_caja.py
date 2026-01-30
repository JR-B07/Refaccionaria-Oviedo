"""
Script de prueba para la funcionalidad de Arqueos de Caja
Ejecutar con: python test_arqueos_caja.py
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000/api/v1"
USUARIO_ID = 1
LOCAL_ID = 1

def test_crear_arqueo():
    """Prueba crear un nuevo arqueo"""
    print("\n📝 Probando CREATE ARQUEO...")
    
    payload = {
        "caja": "Caja 1",
        "local_id": LOCAL_ID,
        "usuario_id": USUARIO_ID,
        "turno": "Mañana",
        
        # Montos declarados
        "efectivo_declarado": 5000,
        "cheque_declarado": 1000,
        "tarjeta_declarado": 2000,
        "debito_declarado": 1500,
        "deposito_declarado": 500,
        "credito_declarado": 300,
        "vale_declarado": 200,
        "lealtad_declarado": 100,
        
        # Montos contados (con pequeña diferencia)
        "efectivo_contado": 5050,  # +50
        "cheque_contado": 1000,
        "tarjeta_contado": 2000,
        "debito_contado": 1500,
        "deposito_contado": 500,
        "credito_contado": 300,
        "vale_contado": 200,
        "lealtad_contado": 100,
        
        "observaciones": "Diferencia en efectivo, posible vuelto faltante"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/arqueos/caja", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Arqueo creado exitosamente")
            print(f"   ID: {data.get('id')}")
            print(f"   Diferencia Total: ${data.get('diferencia_total')}")
            return data.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_listar_arqueos():
    """Prueba listar arqueos"""
    print("\n📋 Probando LISTAR ARQUEOS...")
    
    try:
        response = requests.get(f"{BASE_URL}/arqueos/listar")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Se encontraron {len(data)} arqueos")
            for arqueo in data[:3]:  # Mostrar los primeros 3
                print(f"   - Caja: {arqueo.get('caja')}, "
                      f"Total Declarado: ${arqueo.get('total_declarado')}, "
                      f"Diferencia: ${arqueo.get('diferencia_total')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_obtener_arqueo(arqueo_id):
    """Prueba obtener un arqueo específico"""
    if not arqueo_id:
        print("\n⏭️  Saltando test de obtener arqueo (no hay ID)")
        return
    
    print(f"\n🔍 Probando OBTENER ARQUEO {arqueo_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/arqueos/caja/{arqueo_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Arqueo obtenido exitosamente")
            print(f"   Caja: {data.get('caja')}")
            print(f"   Turno: {data.get('turno')}")
            print(f"   Total Declarado: ${data.get('total_declarado')}")
            print(f"   Total Contado: ${data.get('total_contado')}")
            print(f"   Diferencia Total: ${data.get('diferencia_total')}")
            print(f"   Estado: {'Reconciliado' if data.get('reconciliado') else 'Pendiente'}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_actualizar_arqueo(arqueo_id):
    """Prueba actualizar un arqueo"""
    if not arqueo_id:
        print("\n⏭️  Saltando test de actualizar arqueo (no hay ID)")
        return
    
    print(f"\n✏️  Probando ACTUALIZAR ARQUEO {arqueo_id}...")
    
    payload = {
        "efectivo_contado": 5075,  # Actualizar el monto contado
        "observaciones": "Diferencia corregida después de reconteo",
        "reconciliado": False
    }
    
    try:
        response = requests.put(f"{BASE_URL}/arqueos/caja/{arqueo_id}", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Arqueo actualizado exitosamente")
            print(f"   Nueva diferencia en efectivo: ${data.get('diferencia_efectivo')}")
            print(f"   Nueva diferencia total: ${data.get('diferencia_total')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_listar_con_filtros():
    """Prueba listar arqueos con filtros"""
    print("\n🔎 Probando LISTAR CON FILTROS...")
    
    try:
        # Filtrar por caja
        response = requests.get(f"{BASE_URL}/arqueos/listar?caja=Caja 1")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtro por caja: encontrados {len(data)} arqueos")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS - Sistema de Arqueos de Caja")
    print("=" * 60)
    
    # Verificar que el servidor está corriendo
    try:
        response = requests.get(f"{BASE_URL}/arqueos/listar")
    except:
        print("\n❌ ERROR: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor está corriendo: python run.py")
        return
    
    # Ejecutar pruebas
    arqueo_id = test_crear_arqueo()
    test_listar_arqueos()
    test_obtener_arqueo(arqueo_id)
    test_actualizar_arqueo(arqueo_id)
    test_listar_con_filtros()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60)

if __name__ == "__main__":
    main()
