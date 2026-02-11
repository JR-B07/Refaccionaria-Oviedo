#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para generar un archivo SQL con los INSERT de todos los productos actuales en la BD.
"""

import os
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

def escape_sql_string(value):
    """Escapar valores para SQL"""
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    # Escapar comillas simples
    value_str = str(value).replace("'", "''")
    return f"'{value_str}'"

try:
    print("=" * 80)
    print("GENERANDO SCRIPT SQL DE PRODUCTOS")
    print("=" * 80)
    
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    output_file = "productos_insert.sql"
    
    with engine.connect() as connection:
        # Obtener todos los productos
        query = text("""
            SELECT 
                id, codigo, codigo_barras, nombre, descripcion, marca, modelo,
                categoria, precio_compra, precio_venta, precio_venta_credito,
                stock_total, stock_minimo, ubicacion_estante, ubicacion_fila,
                ubicacion_columna, año_inicio, año_fin
            FROM productos
            ORDER BY id
        """)
        
        result = connection.execute(query)
        productos = result.fetchall()
        
        print(f"\n✅ Se encontraron {len(productos)} productos")
        print(f"📄 Generando archivo: {output_file}\n")
        
        # Generar archivo SQL
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("-- ================================================================\n")
            f.write("-- INSERTS DE PRODUCTOS - REFACCIONARIA OVIEDO\n")
            f.write(f"-- Total de productos: {len(productos)}\n")
            f.write("-- Generado automáticamente\n")
            f.write("-- ================================================================\n\n")
            f.write("USE refaccionaria_db;\n\n")
            
            for i, row in enumerate(productos, 1):
                # Crear el INSERT
                values = []
                
                # id
                values.append(escape_sql_string(row[0]))
                # codigo
                values.append(escape_sql_string(row[1]))
                # codigo_barras
                values.append(escape_sql_string(row[2]))
                # nombre
                values.append(escape_sql_string(row[3]))
                # descripcion
                values.append(escape_sql_string(row[4]))
                # marca
                values.append(escape_sql_string(row[5]))
                # modelo
                values.append(escape_sql_string(row[6]))
                # categoria
                values.append(escape_sql_string(row[7]))
                # precio_compra
                values.append(escape_sql_string(row[8]))
                # precio_venta
                values.append(escape_sql_string(row[9]))
                # precio_venta_credito
                values.append(escape_sql_string(row[10]))
                # stock_total
                values.append(escape_sql_string(row[11]))
                # stock_minimo
                values.append(escape_sql_string(row[12]))
                # ubicacion_estante
                values.append(escape_sql_string(row[13]))
                # ubicacion_fila
                values.append(escape_sql_string(row[14]))
                # ubicacion_columna
                values.append(escape_sql_string(row[15]))
                # año_inicio
                values.append(escape_sql_string(row[16]))
                # año_fin
                values.append(escape_sql_string(row[17]))
                
                insert_sql = f"""INSERT INTO productos (id, codigo, codigo_barras, nombre, descripcion, marca, modelo, categoria, precio_compra, precio_venta, precio_venta_credito, stock_total, stock_minimo, ubicacion_estante, ubicacion_fila, ubicacion_columna, año_inicio, año_fin)
VALUES ({', '.join(values)});
"""
                f.write(insert_sql)
                
                if i % 10 == 0:
                    f.write("\n")
                    print(f"   Procesados: {i}/{len(productos)}")
        
        print(f"\n✅ Archivo generado exitosamente: {output_file}")
        print("=" * 80)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
