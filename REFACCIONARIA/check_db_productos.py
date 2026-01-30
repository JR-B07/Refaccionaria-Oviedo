#!/usr/bin/env python3
import sqlite3
import os

db_path = "refaccionaria.db"

if not os.path.exists(db_path):
    print(f"Base de datos no encontrada en {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar si la tabla existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
if not cursor.fetchone():
    print("Tabla 'productos' no existe")
    conn.close()
    exit(1)

# Contar total de productos
cursor.execute("SELECT COUNT(*) FROM productos")
total = cursor.fetchone()[0]
print(f"Total de productos en la BD: {total}")

if total > 0:
    print("\nPrimeros 5 productos:")
    cursor.execute("SELECT codigo, nombre, stock_total, precio_compra, precio_venta FROM productos LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row}")
else:
    print("No hay productos en la base de datos")

conn.close()
