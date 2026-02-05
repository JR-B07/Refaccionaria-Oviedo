#!/usr/bin/env python
"""
Script para verificar el perfil 'sucursal1' en la BD
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Importar configuración de la app
    from app.core.config import settings
    from app.core.database import SessionLocal
    from app.models.usuario import Usuario
    
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE USUARIO: sucursal1")
    print("=" * 60)
    
    # Configuración de BD
    print(f"\n📊 Configuración de Base de Datos:")
    print(f"   Host: {settings.MYSQL_SERVER}")
    print(f"   Usuario: {settings.MYSQL_USER}")
    print(f"   BD: {settings.MYSQL_DB}")
    print(f"   Puerto: {settings.MYSQL_PORT}")
    
    # Conectar a BD
    print(f"\n📡 Conectando a MySQL...")
    db = SessionLocal()
    
    # Buscar usuario sucursal1
    print(f"\n🔎 Buscando usuario 'sucursal1'...")
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == 'sucursal1').first()
    
    if usuario:
        print(f"\n✅ USUARIO ENCONTRADO:")
        print(f"   ID: {usuario.id}")
        print(f"   Nombre Usuario: {usuario.nombre_usuario}")
        print(f"   Nombre: {usuario.nombre}")
        print(f"   Email: {usuario.email}")
        print(f"   Rol: {usuario.rol}")
        print(f"   Estado: {usuario.estado}")
        print(f"   Local ID: {usuario.local_id}")
    else:
        print(f"\n❌ USUARIO NO ENCONTRADO")
        print(f"   El usuario 'sucursal1' no existe en la base de datos.")
        print(f"\n   Para crear este usuario, ejecuta:")
        print(f"   python reset_admin.py")
    
    # Listar todos los usuarios
    print(f"\n📋 USUARIOS EN LA BASE DE DATOS:")
    usuarios = db.query(Usuario).all()
    
    if usuarios:
        print(f"   Total: {len(usuarios)} usuarios")
        for u in usuarios:
            print(f"   - {u.nombre_usuario} ({u.nombre}) [{u.rol}]")
    else:
        print(f"   ⚠️  No hay usuarios creados")
    
    db.close()
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nPosibles causas:")
    print(f"1. MySQL no está corriendo")
    print(f"2. Base de datos no ha sido inicializada")
    print(f"3. Credenciales incorrectas en .env")
    sys.exit(1)
