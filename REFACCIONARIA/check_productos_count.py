#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para verificar la cantidad de productos en la base de datos"""

import os
import sys
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

try:
    print("=" * 80)
    print("VERIFICACIÓN DE PRODUCTOS EN BASE DE DATOS")
    print("=" * 80)
    
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        print("\n✅ Conectado a la base de datos\n")
        
        # Contar total de productos
        query_total = text("SELECT COUNT(*) as total FROM productos")
        result_total = connection.execute(query_total)
        total = result_total.fetchone()[0]
        
        print(f"📦 TOTAL DE PRODUCTOS: {total}")
        
        # Obtener estadísticas adicionales
        query_stats = text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN precio_compra > 0 THEN 1 END) as con_precio_compra,
                COUNT(CASE WHEN precio_venta > 0 THEN 1 END) as con_precio_venta,
                MIN(precio_venta) as precio_min,
                MAX(precio_venta) as precio_max,
                AVG(precio_venta) as precio_promedio
            FROM productos
        """)
        result_stats = connection.execute(query_stats)
        stats = result_stats.fetchone()
        
        print("\n" + "=" * 80)
        print("ESTADÍSTICAS DE PRODUCTOS")
        print("=" * 80)
        print(f"📊 Total:                {stats[0]}")
        print(f"💰 Con precio de compra: {stats[1]}")
        print(f"💵 Con precio de venta:  {stats[2]}")
        if stats[3] and stats[4] and stats[5]:
            print(f"💲 Precio mínimo:        ${stats[3]:.2f}")
            print(f"💲 Precio máximo:        ${stats[4]:.2f}")
            print(f"💲 Precio promedio:      ${stats[5]:.2f}")
        
        # Mostrar algunos productos de ejemplo
        print("\n" + "=" * 80)
        print("MUESTRA DE PRODUCTOS (primeros 10)")
        print("=" * 80)
        
        query_sample = text("""
            SELECT 
                id,
                nombre,
                codigo,
                precio_venta
            FROM productos
            ORDER BY id
            LIMIT 10
        """)
        result_sample = connection.execute(query_sample)
        
        print(f"{'ID':<6} | {'Código':<15} | {'Nombre':<40} | {'Precio':<10}")
        print("-" * 80)
        
        for row in result_sample:
            id_prod = row[0]
            nombre = row[1][:40] if row[1] else "Sin nombre"
            codigo = row[2] if row[2] else "Sin código"
            precio = f"${row[3]:.2f}" if row[3] else "N/A"
            
            print(f"{id_prod:<6} | {codigo:<15} | {nombre:<40} | {precio:<10}")
        
        print("-" * 80)
        
        # Verificar inventario
        print("\n" + "=" * 80)
        print("ESTADÍSTICAS DE INVENTARIO POR LOCAL")
        print("=" * 80)
        
        query_inventario = text("""
            SELECT 
                l.nombre as local_nombre,
                COUNT(DISTINCT i.producto_id) as productos_con_stock,
                SUM(i.stock) as total_unidades,
                SUM(i.stock_reservado) as unidades_reservadas
            FROM inventario_local i
            JOIN locales l ON i.local_id = l.id
            GROUP BY l.id, l.nombre
            ORDER BY l.id
        """)
        result_inventario = connection.execute(query_inventario)
        
        total_productos_inventario = 0
        total_unidades_global = 0
        
        for row in result_inventario:
            local = row[0]
            productos = row[1]
            unidades = row[2] if row[2] else 0
            reservadas = row[3] if row[3] else 0
            disponibles = unidades - reservadas
            print(f"🏪 {local:<30}")
            print(f"   📦 {productos} productos | 📊 {unidades} unidades | 🔒 {reservadas} reservadas | ✅ {disponibles} disponibles")
            total_productos_inventario += productos
            total_unidades_global += unidades
        
        if total_productos_inventario > 0:
            print(f"\n📈 TOTAL GENERAL: {total_unidades_global} unidades en inventario")
        
        print("\n" + "=" * 80)
        
        if total >= 100:
            print(f"✅ SÍ, hay {total} productos en la base de datos (≥100)")
        else:
            print(f"⚠️  NO, solo hay {total} productos en la base de datos (<100)")
            print(f"   Faltan {100 - total} productos para llegar a 100")
        
        print("=" * 80)
        
except Exception as e:
    print(f"\n❌ Error al consultar la base de datos: {e}")
    sys.exit(1)
