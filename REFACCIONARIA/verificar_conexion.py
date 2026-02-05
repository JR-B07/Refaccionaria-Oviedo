"""
Script para verificar la conexión a MySQL y diagnosticar problemas
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🔍 DIAGNÓSTICO DE CONEXIÓN")
print("=" * 60)

# 1. Verificar configuración
print("\n1️⃣ Verificando configuración...")
try:
    from app.core.config import settings
    print(f"   ✅ Configuración cargada")
    print(f"   📌 MySQL Server: {settings.MYSQL_SERVER}")
    print(f"   📌 MySQL Port: {settings.MYSQL_PORT}")
    print(f"   📌 MySQL User: {settings.MYSQL_USER}")
    print(f"   📌 MySQL Database: {settings.MYSQL_DB}")
    print(f"   📌 Database URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"   ❌ Error al cargar configuración: {e}")
    input("\nPresiona Enter para salir...")
    sys.exit(1)

# 2. Verificar si MySQL está corriendo
print("\n2️⃣ Verificando servicio MySQL...")
import subprocess
try:
    # Intentar con MySQL
    result = subprocess.run(['sc', 'query', 'MySQL'], 
                          capture_output=True, text=True)
    if 'RUNNING' in result.stdout:
        print("   ✅ Servicio MySQL está corriendo")
    elif result.returncode == 0:
        print("   ⚠️  Servicio MySQL existe pero no está corriendo")
        print("   💡 Intenta ejecutar como administrador: net start MySQL")
    else:
        # Intentar con MySQL80
        result = subprocess.run(['sc', 'query', 'MySQL80'], 
                              capture_output=True, text=True)
        if 'RUNNING' in result.stdout:
            print("   ✅ Servicio MySQL80 está corriendo")
        elif result.returncode == 0:
            print("   ⚠️  Servicio MySQL80 existe pero no está corriendo")
            print("   💡 Intenta ejecutar como administrador: net start MySQL80")
        else:
            print("   ❌ No se encontró servicio MySQL instalado")
            print("   💡 Instala MySQL Server desde: https://dev.mysql.com/downloads/installer/")
except Exception as e:
    print(f"   ⚠️  No se pudo verificar servicio: {e}")

# 3. Verificar conexión directa
print("\n3️⃣ Intentando conectar a MySQL...")
try:
    import pymysql
    connection = pymysql.connect(
        host=settings.MYSQL_SERVER,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DB
    )
    print("   ✅ Conexión exitosa con PyMySQL")
    
    # Probar una consulta simple
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"   📌 Versión MySQL: {version[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()
    print(f"   📌 Usuarios en BD: {count[0]}")
    
    cursor.close()
    connection.close()
    
except ImportError:
    print("   ❌ PyMySQL no está instalado")
    print("   💡 Instala con: pip install pymysql")
except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    print("\n   Posibles causas:")
    print("   • MySQL no está corriendo")
    print("   • Usuario/contraseña incorrectos")
    print("   • Base de datos no existe")
    print("   • Puerto 3306 bloqueado")

# 4. Verificar SQLAlchemy
print("\n4️⃣ Verificando SQLAlchemy...")
try:
    from sqlalchemy import create_engine, text
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("   ✅ Conexión exitosa con SQLAlchemy")
except Exception as e:
    print(f"   ❌ Error con SQLAlchemy: {e}")

# 5. Verificar puerto 8001
print("\n5️⃣ Verificando puerto 8001...")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 8001))
if result == 0:
    print("   ⚠️  Puerto 8001 ya está en uso")
    print("   💡 Cierra otras instancias de la aplicación")
else:
    print("   ✅ Puerto 8001 disponible")
sock.close()

print("\n" + "=" * 60)
print("✅ DIAGNÓSTICO COMPLETADO")
print("=" * 60)

input("\nPresiona Enter para salir...")
