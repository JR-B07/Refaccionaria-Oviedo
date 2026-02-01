#!/usr/bin/env python3
"""Script para agregar sucursales usando SQL directo"""

import mysql.connector
from mysql.connector import Error

def agregar_sucursales():
    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='refaccionaria_db'
        )
        
        cursor = conn.cursor()
        
        # Verificar si las sucursales ya existen
        cursor.execute("SELECT COUNT(*) FROM locales WHERE nombre = %s", ("Refaccionaria Oviedo",))
        refaccionaria_existe = cursor.fetchone()[0] > 0
        
        cursor.execute("SELECT COUNT(*) FROM locales WHERE nombre = %s", ("Filtros y Lubricantes",))
        filtros_existe = cursor.fetchone()[0] > 0
        
        # Insertar Refaccionaria Oviedo si no existe
        if not refaccionaria_existe:
            cursor.execute("""
                INSERT INTO locales (nombre, direccion, telefono, email)
                VALUES (%s, %s, %s, %s)
            """, ("Refaccionaria Oviedo", "Ubicación Principal", "", ""))
            print("✅ Sucursal 'Refaccionaria Oviedo' agregada")
        else:
            print("ℹ️ Sucursal 'Refaccionaria Oviedo' ya existe")
        
        # Insertar Filtros y Lubricantes si no existe
        if not filtros_existe:
            cursor.execute("""
                INSERT INTO locales (nombre, direccion, telefono, email)
                VALUES (%s, %s, %s, %s)
            """, ("Filtros y Lubricantes", "Ubicación Secundaria", "", ""))
            print("✅ Sucursal 'Filtros y Lubricantes' agregada")
        else:
            print("ℹ️ Sucursal 'Filtros y Lubricantes' ya existe")
        
        # Commit de cambios
        conn.commit()
        print("\n✅ Sucursales configuradas correctamente")
        
        # Mostrar todas las sucursales
        cursor.execute("SELECT id, nombre FROM locales ORDER BY id")
        sucursales = cursor.fetchall()
        print("\nSucursales en el sistema:")
        for suc_id, nombre in sucursales:
            print(f"  - ID {suc_id}: {nombre}")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    agregar_sucursales()
