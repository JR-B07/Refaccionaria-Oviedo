#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para migrar las contraseñas de bcrypt a SHA256 en la base de datos.
IMPORTANTE: Ejecuta este script solo UNA vez después de cambiar el código.
"""

import os
import sys
import hashlib
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def get_database_url() -> str:
    """Construir URL de conexión a base de datos"""
    user = os.getenv("MYSQL_USER", "root").strip()
    password = os.getenv("MYSQL_PASSWORD", "").strip()
    host = os.getenv("MYSQL_SERVER", "localhost").strip()
    port = os.getenv("MYSQL_PORT", "3306").strip()
    database = os.getenv("MYSQL_DB", "refaccionaria_db").strip()
    
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    else:
        return f"mysql+pymysql://{user}@{host}:{port}/{database}"

def hash_password(password: str) -> str:
    """Generar hash SHA256 de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

# Mapeo de usuarios conocidos con sus contraseñas en texto plano
# NOTA: Ajusta esto según tus usuarios actuales
USUARIOS_CONOCIDOS = {
    'admin': 'admin',
    'sucursal1': 'sucursal1', 
    'sucursal2': 'sucursal2',
    'maria': 'password123',
    'carlos': 'password123',
}

def migrar_contraseñas():
    """Migrar contraseñas de bcrypt a SHA256"""
    
    print("=" * 80)
    print("MIGRACIÓN DE CONTRASEÑAS: BCRYPT -> SHA256")
    print("=" * 80)
    print("\n⚠️  ADVERTENCIA: Este script actualizará las contraseñas en la base de datos.")
    print("   Asegúrate de tener un respaldo antes de continuar.\n")
    
    respuesta = input("¿Deseas continuar? (si/no): ").strip().lower()
    if respuesta not in ['si', 's', 'yes', 'y']:
        print("❌ Migración cancelada")
        return
    
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)
        
        print("\n🔄 Conectando a la base de datos...")
        
        with engine.connect() as connection:
            print("✅ Conexión establecida\n")
            
            usuarios_actualizados = 0
            
            for username, password_plano in USUARIOS_CONOCIDOS.items():
                try:
                    # Generar nuevo hash SHA256
                    nuevo_hash = hash_password(password_plano)
                    
                    # Actualizar en la base de datos
                    update_query = text("""
                        UPDATE usuarios 
                        SET clave_hash = :nuevo_hash 
                        WHERE nombre_usuario = :username
                    """)
                    
                    result = connection.execute(update_query, {
                        'nuevo_hash': nuevo_hash,
                        'username': username
                    })
                    
                    connection.commit()
                    
                    if result.rowcount > 0:
                        print(f"   ✅ Usuario '{username}' actualizado")
                        usuarios_actualizados += 1
                    else:
                        print(f"   ⚠️  Usuario '{username}' no encontrado en la BD")
                        
                except Exception as e:
                    print(f"   ❌ Error actualizando usuario '{username}': {e}")
            
            print(f"\n{'=' * 80}")
            print(f"✅ Migración completada: {usuarios_actualizados} usuarios actualizados")
            print(f"{'=' * 80}\n")
            
            # Mostrar los nuevos hashes
            print("📋 Nuevos hashes SHA256 generados:")
            print("-" * 80)
            for username, password_plano in USUARIOS_CONOCIDOS.items():
                hash_val = hash_password(password_plano)
                print(f"   {username:15} -> {hash_val}")
            print("-" * 80)
            
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrar_contraseñas()
