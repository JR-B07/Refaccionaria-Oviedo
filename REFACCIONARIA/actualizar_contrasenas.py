#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para actualizar contraseñas de usuarios a valores simples.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def get_database_url_with_password() -> str:
    """Construir URL de conexión a base de datos con password"""
    user = os.getenv("MYSQL_USER", "root").strip()
    password = os.getenv("MYSQL_PASSWORD", "root").strip()
    host = os.getenv("MYSQL_SERVER", "localhost").strip()
    port = os.getenv("MYSQL_PORT", "3306").strip()
    database = os.getenv("MYSQL_DB", "refaccionaria_db").strip()
    
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    else:
        return f"mysql+pymysql://{user}@{host}:{port}/{database}"

# Hashes bcrypt para las nuevas contraseñas
HASHES = {
    'admin': '$2b$12$vGQTHL2wS0snxC4/uO4ceeki4nmAMP4RHK6PO4qA5/4iCQdNGPLV.',
    'sucursal1': '$2b$12$N6Zi49AKunHqDrbSWrdw/OACnIgYc/qS8KS3ZzZO0X8W3Ba9kmrku',
    'sucursal2': '$2b$12$GwhoV0TZIrwanLxvYGek8e1qWzdYD9bWF8R6YVT2e5koxUlnDRltW',
}

try:
    database_url = get_database_url_with_password()
    engine = create_engine(database_url)
    connection = engine.connect()
    
    print("=" * 80)
    print("ACTUALIZANDO CONTRASEÑAS")
    print("=" * 80 + "\n")
    
    for username, hash_val in HASHES.items():
        update_query = text("""
            UPDATE usuarios 
            SET clave_hash = :hash 
            WHERE nombre_usuario = :user
        """)
        
        result = connection.execute(update_query, {
            'hash': hash_val,
            'user': username
        })
        
        if result.rowcount > 0:
            print(f"✅ Contraseña de '{username}' actualizada")
        else:
            print(f"⚠️  Usuario '{username}' no encontrado")
    
    connection.commit()
    connection.close()
    
    print("\n" + "=" * 80)
    print("✅ CONTRASEÑAS ACTUALIZADAS EXITOSAMENTE")
    print("=" * 80)
    print("\n📝 Nuevas credenciales:")
    print("   Usuario: admin      | Contraseña: admin")
    print("   Usuario: sucursal1  | Contraseña: sucursal1")
    print("   Usuario: sucursal2  | Contraseña: sucursal2")
    print()
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nAsegúrate de que MySQL esté corriendo en Laragon")
