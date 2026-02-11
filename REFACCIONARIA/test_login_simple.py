#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script simple para verificar login"""

import requests

print("Verificando login en: http://localhost:8000/login")

try:
    response = requests.get("http://localhost:8000/login", timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ El login está funcionando correctamente")
        print(f"Tamaño de página: {len(response.content)} bytes")
        
        # Verificar elementos clave
        if b"loginForm" in response.content:
            print("✅ Formulario de login presente")
        if b"login.css" in response.content:
            print("✅ CSS de login referenciado")
        if b"login.js" in response.content:
            print("✅ JavaScript de login referenciado")
            
    else:
        print(f"❌ Error: Status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error de conexión: {e}")
