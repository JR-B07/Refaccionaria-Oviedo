#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar campos de usuarios"""

import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()

print("=" * 70)
print("VERIFICACIÓN DE DATOS DE USUARIOS")
print("=" * 70)

usuarios = db.query(Usuario).all()
print(f"\nTotal de usuarios: {len(usuarios)}\n")

for u in usuarios:
    print(f"ID: {u.id}")
    print(f"  Nombre: '{u.nombre}'")
    print(f"  Apellido paterno: '{u.apellido_paterno}'")
    print(f"  Apellido materno: '{u.apellido_materno}'")
    print(f"  Nombre completo: '{u.nombre_completo}'")
    print()

db.close()

print("=" * 70)
