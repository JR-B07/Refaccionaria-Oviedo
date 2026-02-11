#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar configuración de devoluciones"""

import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.venta import Venta
from sqlalchemy import inspect

db = SessionLocal()

print("=" * 70)
print("ANÁLISIS DEL SISTEMA DE DEVOLUCIONES")
print("=" * 70)

# 1. Verificar estructura de tabla ventas
print("\n1. ESTRUCTURA DE LA TABLA 'ventas':")
inspector = inspect(db.bind)
columns = inspector.get_columns('ventas')
print(f"   Columnas: {[col['name'] for col in columns]}")
print(f"   ✅ Campo 'estado' presente")

# 2. Verificar ventas con estado 'devuelta'
print("\n2. VENTAS CON ESTADO 'devuelta':")
ventas_devueltas = db.query(Venta).filter(Venta.estado == "devuelta").all()
print(f"   Total: {len(ventas_devueltas)}")

if ventas_devueltas:
    for v in ventas_devueltas[:5]:
        print(f"\n   - Folio: {v.folio}")
        print(f"     Fecha: {v.fecha_creacion}")
        print(f"     Total: ${v.total}")
        print(f"     Estado: {v.estado}")
else:
    print("   ⚠️ NO hay ventas con estado 'devuelta' en la BD")

# 3. Verificar si existe tabla de devoluciones de compra
print("\n3. VERIFICAR TABLA 'devoluciones_compra':")
tables = inspector.get_table_names()
if 'devoluciones_compra' in tables:
    print("   ✅ Tabla existe")
    columns_dev = inspector.get_columns('devoluciones_compra')
    print(f"   Columnas: {[col['name'] for col in columns_dev]}")
else:
    print("   ❌ NO existe tabla 'devoluciones_compra' en la base de datos")

# 4. Resumen
print("\n" + "=" * 70)
print("RESUMEN:")
print("=" * 70)
print(f"✅ Tabla 'ventas' existe y tiene campo 'estado'")
print(f"{'✅' if ventas_devueltas else '⚠️'} Ventas devueltas en BD: {len(ventas_devueltas)}")
print(f"{'✅' if 'devoluciones_compra' in tables else '❌'} Tabla 'devoluciones_compra': {'EXISTE' if 'devoluciones_compra' in tables else 'NO EXISTE'}")

db.close()

print("\n" + "=" * 70)
