#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para crear usuarios administrador y de sucursales en la base de datos.
Ejecutar después de que MySQL esté corriendo: python crear_usuarios.py
"""

import os
import sys
import hashlib
from datetime import datetime
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
    
    print(f"   📌 Configuración: user={user}, pass={'***' if password else '(vacío)'}, host={host}, port={port}, db={database}")
    
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    else:
        # Intentar sin contraseña primero
        return f"mysql+pymysql://{user}@{host}:{port}/{database}"

def hash_password(password: str) -> str:
    """Generar hash SHA256 de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def crear_usuarios():
    """Crear usuarios en la base de datos"""
    
    print("=" * 80)
    print("CREANDO USUARIOS EN LA BASE DE DATOS")
    print("=" * 80)
    
    # Obtener URL de conexión
    database_url = get_database_url()
    
    # Conectar a la base de datos
    engine = None
    connection = None
    
    # Intentar con diferentes contraseñas si falla
    passwords_to_try = ["", "laragon", "root", "admin", "1234"]
    
    for attempt, test_password in enumerate(passwords_to_try, 1):
        try:
            user = os.getenv("MYSQL_USER", "root").strip()
            host = os.getenv("MYSQL_SERVER", "localhost").strip()
            port = os.getenv("MYSQL_PORT", "3306").strip()
            database = os.getenv("MYSQL_DB", "refaccionaria_db").strip()
            
            if test_password:
                test_url = f"mysql+pymysql://{user}:{test_password}@{host}:{port}/{database}"
            else:
                test_url = f"mysql+pymysql://{user}@{host}:{port}/{database}"
            
            print(f"\n   Intento {attempt}: Conectando con password='{test_password}'...")
            engine = create_engine(test_url, pool_pre_ping=True)
            connection = engine.connect()
            print(f"✅ Conexión exitosa a MySQL")
            print(f"   Base de datos: {database}")
            break
            
        except Exception as e:
            if attempt == len(passwords_to_try):
                # Última tentativa falló
                print(f"❌ Error al conectar a la base de datos:")
                print(f"   {str(e)}")
                print("\n⚠️  SOLUCIÓN:")
                print("   1. ¿Laragon está corriendo? Abre C:\\laragon\\laragon.exe")
                print("   2. Haz clic en 'Start All' y espera a que MySQL esté verde ✅")
                print("   3. Si MySQL tiene contraseña, actualiza .env con MYSQL_PASSWORD")
                print("   4. Vuelve a ejecutar: python crear_usuarios.py")
                return False
            # Continuar con siguiente contraseña
            continue
    
    if not connection:
        return False
    
    # Definir usuarios a crear
    usuarios_data = [
        {
            'nombre': 'Administrador',
            'apellido_paterno': 'Sistema',
            'apellido_materno': 'Admin',
            'nombre_usuario': 'admin',
            'password': 'admin123',
            'email': 'admin@refaccionaria.com',
            'rol': 'administrador',
            'local_id': 1,
        },
        {
            'nombre': 'Usuario',
            'apellido_paterno': 'Sucursal',
            'apellido_materno': 'Uno',
            'nombre_usuario': 'sucursal1',
            'password': 'sucursal123',
            'email': 'sucursal1@refaccionaria.com',
            'rol': 'vendedor',
            'local_id': 1,
        },
        {
            'nombre': 'Usuario',
            'apellido_paterno': 'Sucursal',
            'apellido_materno': 'Dos',
            'nombre_usuario': 'sucursal2',
            'password': 'sucursal123',
            'email': 'sucursal2@refaccionaria.com',
            'rol': 'vendedor',
            'local_id': 2,
        },
        {
            'nombre': 'Usuario',
            'apellido_paterno': 'Almacén',
            'apellido_materno': 'Sistema',
            'nombre_usuario': 'almacenero',
            'password': 'almacen123',
            'email': 'almacenero@refaccionaria.com',
            'rol': 'almacenista',
            'local_id': 1,
        },
    ]
    
    # Crear cada usuario
    usuarios_creados = []
    for usuario_data in usuarios_data:
        nombre = usuario_data['nombre_usuario']
        password = usuario_data.pop('password')
        
        try:
            # Verificar si ya existe
            query = text("SELECT id FROM usuarios WHERE nombre_usuario = :nombre")
            result = connection.execute(query, {"nombre": nombre})
            if result.fetchone():
                print(f"⚠️  Usuario '{nombre}' ya existe en BD - saltando...")
                continue
            
            # Hash de contraseña
            password_hash = hash_password(password)
            
            # Insertar nuevo usuario
            insert_query = text("""
                INSERT INTO usuarios (
                    nombre, apellido_paterno, apellido_materno,
                    nombre_usuario, clave_hash, email, rol, 
                    local_id, estado
                ) VALUES (
                    :nombre, :apellido_paterno, :apellido_materno,
                    :nombre_usuario, :clave_hash, :email, :rol,
                    :local_id, 'activo'
                )
            """)
            
            connection.execute(insert_query, {
                'nombre': usuario_data['nombre'],
                'apellido_paterno': usuario_data['apellido_paterno'],
                'apellido_materno': usuario_data['apellido_materno'],
                'nombre_usuario': usuario_data['nombre_usuario'],
                'clave_hash': password_hash,
                'email': usuario_data['email'],
                'rol': usuario_data['rol'],
                'local_id': usuario_data['local_id'],
            })
            
            usuarios_creados.append((nombre, password))
            print(f"✅ Usuario '{nombre}' creado")
            
        except Exception as e:
            print(f"❌ Error al crear usuario '{nombre}': {str(e)}")
            connection.close()
            return False
    
    # Guardar cambios
    try:
        connection.commit()
        print(f"\n✅ {len(usuarios_creados)} usuario(s) guardado(s) exitosamente")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Error al guardar cambios: {str(e)}")
        connection.close()
        return False

def verificar_usuarios():
    """Verificar usuarios creados"""
    print("\n" + "=" * 80)
    print("VERIFICANDO USUARIOS EN LA BD")
    print("=" * 80)
    
    database_url = get_database_url()
    
    try:
        # Conectar con la misma contraseña que funcionó
        for test_password in ["", "laragon", "root", "admin"]:
            try:
                user = os.getenv("MYSQL_USER", "root").strip()
                host = os.getenv("MYSQL_SERVER", "localhost").strip()
                port = os.getenv("MYSQL_PORT", "3306").strip()
                database = os.getenv("MYSQL_DB", "refaccionaria_db").strip()
                
                if test_password:
                    test_url = f"mysql+pymysql://{user}:{test_password}@{host}:{port}/{database}"
                else:
                    test_url = f"mysql+pymysql://{user}@{host}:{port}/{database}"
                
                engine = create_engine(test_url, pool_pre_ping=True)
                connection = engine.connect()
                break
            except:
                continue
        
        # Obtener usuarios
        query = text("SELECT id, nombre_usuario, email, rol FROM usuarios ORDER BY id")
        result = connection.execute(query)
        usuarios = result.fetchall()
        
        print(f"\n📊 Total de usuarios: {len(usuarios)}\n")
        
        for usuario in usuarios:
            print(f"  🔹 {usuario[1]:15} | Email: {usuario[2]:25} | Rol: {usuario[3]:15}")
        
        connection.close()
    except Exception as e:
        print(f"❌ Error al verificar: {str(e)}")

if __name__ == "__main__":
    print("\n")
    success = crear_usuarios()
    if success:
        verificar_usuarios()
        print("\n" + "=" * 80)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print("\n📝 Puedes ahora usar las siguientes credenciales para login:")
        print("   Usuario: admin        | Password: admin123")
        print("   Usuario: sucursal1    | Password: sucursal123")
        print("   Usuario: sucursal2    | Password: sucursal123")
        print("   Usuario: almacenero   | Password: almacen123")
        print()
    else:
        print("\n" + "=" * 80)
        print("❌ ERROR: No se pudieron crear los usuarios")
        print("=" * 80)
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Abre Laragon (C:\\laragon\\laragon.exe)")
        print("   2. Haz clic en 'Start All' para iniciar MySQL")
        print("   3. Espera a que MySQL esté verde ✅")
        print("   4. Vuelve a ejecutar: python crear_usuarios.py")
        print()
        sys.exit(1)
