#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostico para Refaccionaria ERP
Verifica la salud general del sistema
"""

import os
import sys
import socket
import subprocess
from pathlib import Path
from datetime import datetime

def print_title(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_item(status, text):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {text}")

def main():
    print_title("DIAGNOSTICO - REFACCIONARIA ERP")
    
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Sistema: {sys.platform}\n")
    
    all_ok = True
    
    # Python
    print_title("PYTHON")
    print_item(True, f"Python ejecutable: {sys.executable}")
    print_item(True, f"Version: {sys.version.split()[0]}")
    
    # Dependencias
    print_title("DEPENDENCIAS")
    deps = ['fastapi', 'uvicorn', 'sqlalchemy', 'pymysql', 'webview', 'requests', 'python-dotenv']
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
            print_item(True, f"{dep}")
        except ImportError:
            print_item(False, f"{dep}")
            all_ok = False
    
    # MySQL
    print_title("MYSQL")
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print_item(True, f"MySQL cliente: {result.stdout.strip()}")
        else:
            print_item(False, "MySQL cliente no encontrado")
            all_ok = False
    except:
        print_item(False, "MySQL cliente no encontrado")
        all_ok = False
    
    # Base de datos
    print_title("BASE DE DATOS")
    try:
        from app.database import SessionLocal, engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print_item(True, "Conexion a MySQL exitosa")
    except Exception as e:
        print_item(False, f"Conexion a MySQL falló: {e}")
        all_ok = False
    
    try:
        from app.models import Producto, Paquete
        from app.database import SessionLocal
        
        db = SessionLocal()
        prod_count = db.query(Producto).count()
        paq_count = db.query(Paquete).count()
        db.close()
        
        print_item(True, f"Productos en BD: {prod_count}")
        print_item(True, f"Paquetes en BD: {paq_count}")
        
        if prod_count == 0:
            print_item(False, "No hay productos cargados")
            all_ok = False
        if paq_count == 0:
            print_item(False, "No hay paquetes cargados")
            all_ok = False
    except Exception as e:
        print_item(False, f"Error verificando BD: {e}")
        all_ok = False
    
    # Estructura
    print_title("ESTRUCTURA DEL PROYECTO")
    archivos = [
        ('app/main.py', 'Main de FastAPI'),
        ('app/models.py', 'Modelos'),
        ('app/database.py', 'Conexion BD'),
        ('launch_desktop.py', 'Launcher Desktop'),
        ('.env', 'Configuracion (opcional)'),
    ]
    
    for archivo, desc in archivos:
        existe = Path(archivo).exists()
        print_item(existe, f"{desc} ({archivo})")
        if not existe and archivo != '.env':
            all_ok = False
    
    # Puerto
    print_title("PUERTO")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8001))
    sock.close()
    puerto_disponible = result != 0
    print_item(puerto_disponible, "Puerto 8001 disponible")
    
    # Resumen
    print_title("RESUMEN")
    if all_ok and puerto_disponible:
        print("\033[92m✓ Todo esta bien. La aplicacion esta lista para iniciar.\033[0m\n")
        return 0
    else:
        print("\033[91m✗ Hay problemas que deben ser resueltos antes de iniciar.\033[0m\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
