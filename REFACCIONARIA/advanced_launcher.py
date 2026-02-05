#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher avanzado para Refaccionaria ERP
Maneja:
- Verificacion de dependencias
- Inicializacion de base de datos
- Inicio del servidor FastAPI
- Control de la ventana de escritorio
"""

import os
import sys
import time
import subprocess
import socket
import threading
from pathlib import Path

# Colores para la consola (Windows compatible)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    
    @staticmethod
    def windows_fix():
        # Para Windows, desactivar colores si no es compatible
        if sys.platform == 'win32':
            os.system('color')


def print_header(text):
    """Imprime un encabezado"""
    print(f"\n{Colors.BLUE}{'='*50}")
    print(f"  {text.upper()}")
    print(f"{'='*50}{Colors.RESET}\n")


def print_success(text):
    """Imprime un mensaje de exito"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Imprime un mensaje de error"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    """Imprime un mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def verificar_puerto(puerto):
    """Verifica si un puerto esta disponible"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', puerto))
    sock.close()
    return result != 0


def verificar_dependencias():
    """Verifica que todas las dependencias esten instaladas"""
    print_header("Verificando Dependencias")
    
    dependencias = ['fastapi', 'uvicorn', 'sqlalchemy', 'pymysql', 'webview', 'requests', 'python-dotenv']
    faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print_success(f"{dep} instalado")
        except ImportError:
            print_warning(f"{dep} no instalado")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\nInstalando dependencias faltantes: {', '.join(faltantes)}\n")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q'] + faltantes)
            print_success("Dependencias instaladas correctamente\n")
            return True
        except Exception as e:
            print_error(f"Error al instalar dependencias: {e}\n")
            return False
    
    print_success("Todas las dependencias estan instaladas\n")
    return True


def verificar_estructura():
    """Verifica que la estructura del proyecto sea correcta"""
    print_header("Verificando Estructura del Proyecto")
    
    archivos_requeridos = [
        'app/main.py',
        'app/models.py',
        'app/database.py',
        'launch_desktop.py'
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print_success(f"{archivo} encontrado")
        else:
            print_error(f"{archivo} no encontrado")
            todos_ok = False
    
    if not todos_ok:
        print_error("\nLa estructura del proyecto esta incompleta\n")
        return False
    
    print_success("Estructura del proyecto correcta\n")
    return True


def verificar_puerto_disponible(puerto=8001):
    """Verifica que el puerto este disponible"""
    print_header(f"Verificando Puerto {puerto}")
    
    if verificar_puerto(puerto):
        print_success(f"Puerto {puerto} disponible\n")
        return True
    else:
        print_error(f"Puerto {puerto} ya esta en uso\n")
        return False


def crear_archivo_env():
    """Crea el archivo .env si no existe"""
    if Path('.env').exists():
        return True
    
    print_header("Creando Configuracion")
    
    config = """DEBUG=true
MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
HOST=127.0.0.1
PORT=8001
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(config)
        print_success(".env creado\n")
        return True
    except Exception as e:
        print_error(f"Error creando .env: {e}\n")
        return False


def inicializar_base_datos():
    """Inicializa la base de datos"""
    print_header("Inicializando Base de Datos")
    
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/inicializar_datos.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(result.stdout)
            print_error(f"Error: {result.stderr}\n")
            return False
    except subprocess.TimeoutExpired:
        print_error("Timeout esperando inicializacion de BD\n")
        return False
    except Exception as e:
        print_error(f"Error inicializando BD: {e}\n")
        return False


def mostrar_informacion_inicio():
    """Muestra informacion de inicio"""
    print_header("Informacion de Inicio")
    print("Aplicacion: Refaccionaria ERP v1.0")
    print("URL: http://127.0.0.1:8001")
    print("API Docs: http://127.0.0.1:8001/docs")
    print("Login: http://127.0.0.1:8001/static/login.html")
    print("\nPara detener el servidor presiona Ctrl+C\n")


def main():
    """Funcion principal"""
    Colors.windows_fix()
    
    print_header("Refaccionaria ERP - Launcher Avanzado")
    
    # Cambiar al directorio del script
    os.chdir(Path(__file__).parent)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print_error("No se pudieron instalar las dependencias\n")
        sys.exit(1)
    
    # Verificar estructura
    if not verificar_estructura():
        print_error("Estructura del proyecto incompleta\n")
        sys.exit(1)
    
    # Crear .env
    crear_archivo_env()
    
    # Verificar puerto
    if not verificar_puerto_disponible(8001):
        print_warning("El puerto 8001 esta en uso. Intenta detener el servidor anterior.\n")
        sys.exit(1)
    
    # Inicializar base de datos
    if not inicializar_base_datos():
        print_warning("Hubo problemas inicializando la BD, pero se continuara...\n")
    
    # Mostrar informacion
    mostrar_informacion_inicio()
    
    # Iniciar launch_desktop.py
    print_header("Iniciando Refaccionaria")
    
    try:
        subprocess.run([sys.executable, 'launch_desktop.py'])
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Deteniendo Refaccionaria...{Colors.RESET}\n")
    except Exception as e:
        print_error(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
