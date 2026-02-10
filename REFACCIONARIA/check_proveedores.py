#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar y listar proveedores"""

from app.core.database import SessionLocal
from app.models.proveedor import Proveedor

db = SessionLocal()
proveedores = db.query(Proveedor).all()

print("=" * 70)
print("PROVEEDORES EN LA BASE DE DATOS")
print("=" * 70)

if proveedores:
    for p in proveedores:
        print(f"ID: {p.id} - Nombre: {p.nombre}")
else:
    print("No hay proveedores. Importando datos de prueba...")
    
    prov_data = [
        Proveedor(clave="PROV001", nombre="DISTRIBUIDORA RAUL", rfc="RFC001"),
        Proveedor(clave="PROV002", nombre="AUTO PARTS PLUS", rfc="RFC002"),
        Proveedor(clave="PROV003", nombre="REFACCIONES GARCIA", rfc="RFC003"),
    ]
    
    for p in prov_data:
        db.add(p)
    
    db.commit()
    print("✅ Proveedores agregados correctamente")

print(f"\nTotal: {len(proveedores)} proveedores")
db.close()
