#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.core.database import SessionLocal
from app.models.compra import Compra
from app.models.usuario import Usuario
from app.models.local import Local

db = SessionLocal()

compras = db.query(Compra).all()
print(f"Total de compras: {len(compras)}")

if compras:
    for c in compras[-5:]:
        print(f"  - Folio: {c.folio}, Estado: {c.estado}, Local ID: {c.local_id}, Usuario ID: {c.usuario_id}, Total: {c.total}")
else:
    print("  No hay compras en la base de datos")

print("\n" + "="*50)

usuarios = db.query(Usuario).all()
print(f"Total de usuarios: {len(usuarios)}")
for u in usuarios[:3]:
    print(f"  - {u.nombre_completo} (ID: {u.id}, Local: {u.local_id})")

print("\n" + "="*50)

locales = db.query(Local).all()
print(f"Total de locales: {len(locales)}")
for l in locales:
    print(f"  - {l.nombre} (ID: {l.id})")

db.close()
