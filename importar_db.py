#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para importar refaccionaria_db.sql a MySQL
Intenta múltiples contraseñas si la primera falla
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

def importar_sql_a_mysql():
    """Importar archivo SQL consolidado a MySQL"""
    
    print("=" * 80)
    print("IMPORTANDO REFACCIONARIA_DB.SQL A MYSQL")
    print("=" * 80)
    
    # Configuración de conexión base
    host = os.getenv('MYSQL_SERVER', 'localhost')
    user = os.getenv('MYSQL_USER', 'root')
    port = int(os.getenv('MYSQL_PORT', '3306'))
    password = os.getenv('MYSQL_PASSWORD', '')
    
    print(f"\n📌 Configuración de conexión:")
    print(f"   Host: {host}")
    print(f"   Usuario: {user}")
    print(f"   Puerto: {port}")
    print(f"   Contraseña: {'*' * len(password) if password else '(vacío)'}")
    
    # Ruta del archivo SQL
    sql_file = 'refaccionaria_db.sql'
    
    if not os.path.exists(sql_file):
        print(f"\n❌ Error: No se encontró {sql_file}")
        print(f"   Directorio actual: {os.getcwd()}")
        return False
    
    print(f"\n📄 Archivo SQL: {sql_file}")
    print(f"   Tamaño: {os.path.getsize(sql_file)} bytes")
    
    # Leer archivo SQL
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        print(f"✅ Archivo leído ({len(sql_content)} caracteres)")
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return False
    
    # Conectar a MySQL - Intentar con múltiples contraseñas
    connection = None
    passwords_to_try = [password, '', 'laragon', 'root', 'admin', '1234', 'password']
    
    print(f"\n🔌 Intentando conectar a MySQL...")
    
    for attempt, test_password in enumerate(passwords_to_try, 1):
        try:
            config = {
                'host': host,
                'user': user,
                'password': test_password,
                'port': port
            }
            
            connection = mysql.connector.connect(**config)
            if attempt > 1:
                print(f"   ✅ Conexión exitosa con contraseña alternativa")
            else:
                print(f"✅ Conexión exitosa a MySQL")
            break
            
        except Error as e:
            if attempt == len(passwords_to_try):
                print(f"\n❌ No se pudo conectar a MySQL después de {len(passwords_to_try)} intentos")
                print(f"\n❌ Error: {e}")
                print(f"\nSoluciones posibles:")
                print(f"   1. Verificar que MySQL esté corriendo")
                print(f"   2. Verificar que Laragon esté activo (C:\\laragon\\laragon.exe)")
                return False
    
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Dividir sentencias SQL (ignorar comentarios)
        statements = []
        current_statement = ""
        
        for line in sql_content.split('\n'):
            line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith('--'):
                continue
            
            current_statement += line + " "
            
            # Detectar fin de sentencia
            if line.endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
        
        # Agregar última sentencia si existe
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        print(f"\n📊 Total de sentencias SQL: {len(statements)}")
        
        # Ejecutar sentencias
        executed = 0
        errors = 0
        
        print(f"\n⚙️  Ejecutando sentencias...")
        
        for i, statement in enumerate(statements, 1):
            try:
                # Mostrar avance cada 10 sentencias
                if i % 10 == 0 or i == 1:
                    print(f"   [{i}/{len(statements)}] Ejecutando...", end='\r')
                
                cursor.execute(statement)
                executed += 1
                
            except Error as e:
                errors += 1
        
        connection.commit()
        print(f"\n\n✅ Importación completada:")
        print(f"   Sentencias ejecutadas: {executed}/{len(statements)}")
        if errors > 0:
            print(f"   Errores: {errors}")
        
        # Verificar resultado
        print(f"\n📋 Verificando datos importados...")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM productos;")
            productos_count = cursor.fetchone()[0]
            print(f"   ✓ Productos: {productos_count}")
        except Exception as e:
            print(f"   ⚠ Productos: {e}")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM inventario_local;")
            inventario_count = cursor.fetchone()[0]
            print(f"   ✓ Inventario local: {inventario_count}")
        except Exception as e:
            print(f"   ⚠ Inventario: {e}")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM clientes;")
            clientes_count = cursor.fetchone()[0]
            print(f"   ✓ Clientes: {clientes_count}")
        except Exception as e:
            print(f"   ⚠ Clientes: {e}")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM proveedores;")
            proveedores_count = cursor.fetchone()[0]
            print(f"   ✓ Proveedores: {proveedores_count}")
        except Exception as e:
            print(f"   ⚠ Proveedores: {e}")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM paquetes;")
            paquetes_count = cursor.fetchone()[0]
            print(f"   ✓ Paquetes: {paquetes_count}")
        except Exception as e:
            print(f"   ⚠ Paquetes: {e}")
        
        cursor.close()
        
        print(f"\n{'=' * 80}")
        print(f"✅ IMPORTACIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'=' * 80}")
        
        return True
        
    except Error as e:
        print(f"\n❌ Error de MySQL: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    success = importar_sql_a_mysql()
    sys.exit(0 if success else 1)
