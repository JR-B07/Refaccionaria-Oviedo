#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar sucursales en la BD"""

from app.core.database import SessionLocal
from app.models.local import Local

db = SessionLocal()
locales = db.query(Local).all()

print("=" * 70)
print("SUCURSALES EN LA BASE DE DATOS")
print("=" * 70)

for local in locales:
    print(f"ID: {local.id} - Nombre: {local.nombre}")

print(f"\nTotal: {len(locales)} sucursales")
db.close()
