#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para consultar y verificar el inventario por producto y sucursal.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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

try:
    print("=" * 80)
    print("CONSULTA DE INVENTARIO POR LOCAL")
    print("=" * 80)
    
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        # Consultar inventario con información detallada
        query = text("""
            SELECT 
                p.codigo,
                p.nombre,
                p.precio_compra,
                p.precio_venta,
                p.stock_total,
                l.nombre as local,
                il.stock,
                il.stock_reservado
            FROM inventario_local il
            JOIN productos p ON il.producto_id = p.id
            JOIN locales l ON il.local_id = l.id
            ORDER BY p.codigo, l.id
            LIMIT 20
        """)
        
        result = connection.execute(query)
        registros = result.fetchall()
        
        print("\n📦 PRIMEROS 20 REGISTROS DE INVENTARIO\n")
        print(f"{'Código':<12} | {'Producto':<30} | {'Local':<25} | {'Stock':<8} | {'Reservado':<10}")
        print("-" * 105)
        
        for reg in registros:
            codigo = reg[0]
            nombre = reg[1][:28]
            local = reg[5][:23]
            stock = reg[6]
            reservado = reg[7]
            
            print(f"{codigo:<12} | {nombre:<30} | {local:<25} | {stock:<8} | {reservado:<10}")
        
        # Productos con más stock
        print("\n" + "=" * 80)
        print("PRODUCTOS CON MAYOR STOCK")
        print("=" * 80)
        
        query_top = text("""
            SELECT 
                p.codigo,
                p.nombre,
                p.stock_total
            FROM productos p
            ORDER BY p.stock_total DESC
            LIMIT 10
        """)
        
        result = connection.execute(query_top)
        top_productos = result.fetchall()
        
        print(f"\n{'Posición':<10} | {'Código':<12} | {'Producto':<40} | {'Stock Total':<12}")
        print("-" * 80)
        
        for i, prod in enumerate(top_productos, 1):
            codigo = prod[0]
            nombre = prod[1][:38]
            stock = prod[2]
            print(f"{i:<10} | {codigo:<12} | {nombre:<40} | {stock:<12}")
        
        # Productos con menos stock
        print("\n" + "=" * 80)
        print("PRODUCTOS CON MENOR STOCK")
        print("=" * 80)
        
        query_bottom = text("""
            SELECT 
                p.codigo,
                p.nombre,
                p.stock_total,
                p.stock_minimo
            FROM productos p
            ORDER BY p.stock_total ASC
            LIMIT 10
        """)
        
        result = connection.execute(query_bottom)
        bottom_productos = result.fetchall()
        
        print(f"\n{'Posición':<10} | {'Código':<12} | {'Producto':<40} | {'Stock':<8} | {'Mínimo':<8}")
        print("-" * 85)
        
        for i, prod in enumerate(bottom_productos, 1):
            codigo = prod[0]
            nombre = prod[1][:38]
            stock = prod[2]
            minimo = prod[3]
            alerta = "⚠️ " if stock < minimo else ""
            print(f"{alerta}{i:<10} | {codigo:<12} | {nombre:<40} | {stock:<8} | {minimo:<8}")
        
        # Resumen por local
        print("\n" + "=" * 80)
        print("RESUMEN POR LOCAL")
        print("=" * 80)
        
        query_resumen = text("""
            SELECT 
                l.nombre as local,
                COUNT(DISTINCT il.producto_id) as productos_diferentes,
                SUM(il.stock) as stock_total,
                SUM(il.stock_reservado) as stock_reservado_total,
                AVG(il.stock) as stock_promedio,
                MIN(il.stock) as stock_minimo_producto,
                MAX(il.stock) as stock_maximo_producto
            FROM inventario_local il
            JOIN locales l ON il.local_id = l.id
            GROUP BY l.id, l.nombre
            ORDER BY l.id
        """)
        
        result = connection.execute(query_resumen)
        resumenes = result.fetchall()
        
        print()
        for res in resumenes:
            print(f"🏢 {res[0]}")
            print(f"   Productos diferentes: {res[1]}")
            print(f"   Stock total: {res[2]:,}")
            print(f"   Stock reservado: {res[3]:,}")
            print(f"   Stock promedio por producto: {res[4]:.2f}")
            print(f"   Stock mínimo (un producto): {res[5]}")
            print(f"   Stock máximo (un producto): {res[6]}")
            print()
        
        print("=" * 80)
        print("✅ Consulta completada exitosamente")
        print("=" * 80)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
