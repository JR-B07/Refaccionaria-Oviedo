#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar el endpoint de login"""

import requests
import sys

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("PRUEBA DE ENDPOINT DE LOGIN")
print("=" * 70)

# 1. Verificar health
print("\n1. Verificando servidor...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   ✅ Status Code: {response.status_code}")
    print(f"   📊 Respuesta: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 2. Verificar página de login
print("\n2. Verificando página de login...")
try:
    response = requests.get(f"{BASE_URL}/login", timeout=5)
    print(f"   ✅ Status Code: {response.status_code}")
    print(f"   📄 Content-Type: {response.headers.get('content-type')}")
    print(f"   📏 Tamaño: {len(response.content)} bytes")
    
    # Verificar si contiene HTML
    if b"<!DOCTYPE html>" in response.content:
        print("   ✅ Es un documento HTML válido")
    else:
        print("   ⚠️  No parece ser HTML")
        
    # Verificar si tiene el formulario de login
    if b"loginForm" in response.content:
        print("   ✅ Contiene el formulario de login")
    else:
        print("   ⚠️  No se encontró el formulario de login")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Verificar archivos estáticos
print("\n3. Verificando archivos estáticos...")
static_files = [
    "/static/css/login.css",
    "/static/js/login.js",
    "/static/images/RefaccionariaLogo.svg.jpg"
]

for file_path in static_files:
    try:
        response = requests.get(f"{BASE_URL}{file_path}", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ {file_path} - {len(response.content)} bytes")
        else:
            print(f"   ❌ {file_path} - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ {file_path} - Error: {e}")

# 4. Verificar endpoint de login API
print("\n4. Verificando endpoint de API de login...")
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
        timeout=5
    )
    print(f"   ✅ Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Login exitoso")
    else:
        print(f"   ⚠️  Login falló: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
