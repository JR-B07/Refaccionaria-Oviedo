#!/usr/bin/env python3
"""Verificar paquetes en la BD"""
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='refaccionaria_db'
    )
    
    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"Conectado a MySQL Server {db_info}")
        
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM paquetes")
        count = cursor.fetchone()[0]
        print(f"\nTotal de paquetes: {count}")
        
        cursor.execute("SELECT id, nombre, clase, descripcion FROM paquetes")
        paquetes = cursor.fetchall()
        if paquetes:
            print("\nPaquetes encontrados:")
            for p in paquetes:
                print(f"  ID: {p[0]}, Nombre: {p[1]}, Clase: {p[2]}, Desc: {p[3]}")
        else:
            print("No hay paquetes en la BD")
        
        cursor.close()
            
except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        connection.close()
