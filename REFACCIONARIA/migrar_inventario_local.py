#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para migrar/poblar la tabla inventario_local.
Asigna stock inicial a cada producto en cada sucursal.
"""

import os
import random
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
    print("MIGRACIÓN DE INVENTARIO LOCAL")
    print("=" * 80)
    
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        # Verificar cuántos registros hay actualmente
        result = connection.execute(text("SELECT COUNT(*) FROM inventario_local"))
        count_actual = result.fetchone()[0]
        print(f"\n📊 Registros actuales en inventario_local: {count_actual}")
        
        # Obtener locales
        result = connection.execute(text("SELECT id, nombre FROM locales ORDER BY id"))
        locales = result.fetchall()
        print(f"\n🏢 Locales encontrados: {len(locales)}")
        for local in locales:
            print(f"   - ID {local[0]}: {local[1]}")
        
        # Obtener productos
        result = connection.execute(text("SELECT id, codigo, nombre FROM productos ORDER BY id"))
        productos = result.fetchall()
        print(f"\n📦 Productos encontrados: {len(productos)}")
        
        if not locales or not productos:
            print("\n⚠️  No hay locales o productos en la base de datos.")
            print("   Por favor, asegúrate de tener locales y productos antes de ejecutar esta migración.")
            exit(1)
        
        print("\n" + "=" * 80)
        print("INICIANDO MIGRACIÓN")
        print("=" * 80)
        
        registros_insertados = 0
        registros_actualizados = 0
        errores = 0
        
        for local in locales:
            local_id = local[0]
            local_nombre = local[1]
            
            print(f"\n🏢 Procesando local: {local_nombre} (ID: {local_id})")
            
            for producto in productos:
                producto_id = producto[0]
                producto_codigo = producto[1]
                producto_nombre = producto[2]
                
                try:
                    # Verificar si ya existe el registro
                    check_query = text("""
                        SELECT id, stock, stock_reservado 
                        FROM inventario_local 
                        WHERE producto_id = :producto_id AND local_id = :local_id
                    """)
                    result = connection.execute(check_query, {
                        "producto_id": producto_id,
                        "local_id": local_id
                    })
                    existing = result.fetchone()
                    
                    if existing:
                        # Ya existe, solo actualizar si el stock es 0
                        if existing[1] == 0:
                            # Generar stock aleatorio entre 5 y 50
                            stock_inicial = random.randint(5, 50)
                            update_query = text("""
                                UPDATE inventario_local 
                                SET stock = :stock 
                                WHERE producto_id = :producto_id AND local_id = :local_id
                            """)
                            connection.execute(update_query, {
                                "stock": stock_inicial,
                                "producto_id": producto_id,
                                "local_id": local_id
                            })
                            connection.commit()
                            registros_actualizados += 1
                    else:
                        # No existe, insertar nuevo registro
                        # Generar stock aleatorio entre 5 y 50
                        stock_inicial = random.randint(5, 50)
                        
                        insert_query = text("""
                            INSERT INTO inventario_local 
                            (producto_id, local_id, stock, stock_reservado) 
                            VALUES (:producto_id, :local_id, :stock, 0)
                        """)
                        connection.execute(insert_query, {
                            "producto_id": producto_id,
                            "local_id": local_id,
                            "stock": stock_inicial
                        })
                        connection.commit()
                        registros_insertados += 1
                    
                except Exception as e:
                    errores += 1
                    print(f"   ❌ Error con producto {producto_codigo}: {str(e)}")
        
        # Actualizar stock_total en productos
        print("\n" + "=" * 80)
        print("ACTUALIZANDO STOCK TOTAL EN PRODUCTOS")
        print("=" * 80)
        
        update_stock_query = text("""
            UPDATE productos p
            SET p.stock_total = (
                SELECT COALESCE(SUM(il.stock), 0)
                FROM inventario_local il
                WHERE il.producto_id = p.id
            )
        """)
        connection.execute(update_stock_query)
        connection.commit()
        print("✅ Stock total actualizado en tabla productos")
        
        # Verificar resultados finales
        result = connection.execute(text("SELECT COUNT(*) FROM inventario_local"))
        count_final = result.fetchone()[0]
        
        print("\n" + "=" * 80)
        print("RESUMEN DE MIGRACIÓN")
        print("=" * 80)
        print(f"✅ Registros insertados: {registros_insertados}")
        print(f"🔄 Registros actualizados: {registros_actualizados}")
        print(f"❌ Errores: {errores}")
        print(f"📊 Total de registros en inventario_local: {count_final}")
        print("=" * 80)
        
        # Mostrar algunas estadísticas
        stats_query = text("""
            SELECT 
                l.nombre as local,
                COUNT(il.id) as productos,
                SUM(il.stock) as stock_total,
                AVG(il.stock) as stock_promedio
            FROM inventario_local il
            JOIN locales l ON il.local_id = l.id
            GROUP BY l.id, l.nombre
            ORDER BY l.id
        """)
        result = connection.execute(stats_query)
        stats = result.fetchall()
        
        print("\n📊 ESTADÍSTICAS POR LOCAL")
        print("-" * 80)
        for stat in stats:
            print(f"🏢 {stat[0]}:")
            print(f"   - Productos registrados: {stat[1]}")
            print(f"   - Stock total: {stat[2]}")
            print(f"   - Stock promedio por producto: {stat[3]:.2f}")
            print()
        
        print("✅ Migración completada exitosamente")
        
except Exception as e:
    print(f"\n❌ Error durante la migración: {e}")
    import traceback
    traceback.print_exc()
