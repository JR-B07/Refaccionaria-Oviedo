#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para exportar TODOS los datos de la base de datos en formato SQL INSERT.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from decimal import Decimal
from datetime import datetime, date

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

def escape_sql_string(value):
    """Escapar cadenas para SQL"""
    if value is None:
        return "NULL"
    if isinstance(value, str):
        value = value.replace("'", "''")
        value = value.replace("\\", "\\\\")
        return f"'{value}'"
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (datetime, date)):
        return f"'{value}'"
    return f"'{value}'"

def exportar_tabla(connection, tabla, descripcion):
    """Exportar datos de una tabla"""
    try:
        # Obtener datos
        query = text(f"SELECT * FROM {tabla}")
        result = connection.execute(query)
        rows = result.fetchall()
        
        if not rows:
            return f"-- No hay datos en {tabla}\n"
        
        # Obtener nombres de columnas
        columns = result.keys()
        
        output = []
        output.append(f"-- ================================================================")
        output.append(f"-- DATOS DE {descripcion.upper()}")
        output.append(f"-- Registros: {len(rows)}")
        output.append(f"-- ================================================================\n")
        
        # Generar INSERTs
        for row in rows:
            values = []
            for i, col in enumerate(columns):
                values.append(escape_sql_string(row[i]))
            
            values_str = ", ".join(values)
            output.append(f"INSERT INTO {tabla} ({', '.join(columns)}) VALUES ({values_str});")
        
        output.append("")
        return "\n".join(output)
        
    except Exception as e:
        return f"-- Error exportando {tabla}: {str(e)}\n"

try:
    print("=" * 80)
    print("EXPORTANDO TODOS LOS DATOS DE LA BASE DE DATOS")
    print("=" * 80)
    
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    sql_output = []
    sql_output.append("-- ================================================================")
    sql_output.append("-- DATOS EXPORTADOS DE refaccionaria_db")
    sql_output.append("-- Fecha de exportación: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_output.append("-- ================================================================\n")
    
    with engine.connect() as connection:
        # Lista de tablas a exportar en orden
        tablas = [
            ("locales", "Sucursales/Locales"),
            ("marcas", "Marcas"),
            ("productos", "Productos"),
            ("inventario_local", "Inventario por Local"),
            ("clientes", "Clientes"),
            ("proveedores", "Proveedores"),
            ("paquetes", "Paquetes"),
            ("paquete_productos", "Productos de Paquetes"),
            ("grupos", "Grupos"),
            ("grupo_productos", "Productos de Grupos"),
            ("grupo_aplicaciones", "Aplicaciones de Grupos"),
        ]
        
        for tabla, descripcion in tablas:
            print(f"\n📊 Exportando {descripcion} ({tabla})...")
            sql_content = exportar_tabla(connection, tabla, descripcion)
            sql_output.append(sql_content)
            print(f"   ✅ Completado")
        
        # Guardar archivo
        output_file = "datos_exportados_inserts.sql"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_output))
        
        print("\n" + "=" * 80)
        print(f"✅ Exportación completada: {output_file}")
        print("=" * 80)
        
        # Contar líneas
        line_count = len(sql_output)
        print(f"\n📊 Total de líneas generadas: {line_count}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
