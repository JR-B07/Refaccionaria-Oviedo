#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar ventas devueltas directamente en la BD"""

from app.core.database import SessionLocal
from app.models.venta import Venta, DetalleVenta

db = SessionLocal()

print("=" * 70)
print("VERIFICACIÓN DIRECTA DE VENTAS DEVUELTAS")
print("=" * 70)

# Consultar ventas devueltas
ventas_devueltas = db.query(Venta).filter(Venta.estado == "devuelta").all()

print(f"\n📊 Total ventas devueltas: {len(ventas_devueltas)}")

if ventas_devueltas:
    print("\n📋 Detalles de las ventas devueltas:\n")
    for i, venta in enumerate(ventas_devueltas, 1):
        print(f"{i}. Folio: {venta.folio}")
        print(f"   ID: {venta.id}")
        print(f"   Estado: {venta.estado}")
        print(f"   Total: ${float(venta.total):,.2f}")
        print(f"   Fecha creación: {venta.fecha_creacion}")
        print(f"   Local ID: {venta.local_id}")
        print(f"   Usuario ID: {venta.usuario_id}")
        print(f"   Cliente ID: {venta.cliente_id}")
        
        # Contar detalles
        detalles = db.query(DetalleVenta).filter(DetalleVenta.venta_id == venta.id).count()
        print(f"   Detalles: {detalles} productos")
        print()
else:
    print("\n❌ No se encontraron ventas devueltas")

db.close()

print("=" * 70)
