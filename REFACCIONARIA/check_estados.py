#!/usr/bin/env python3
"""Script para verificar estados en la base de datos"""

from app.core.database import SessionLocal
from app.models.compra import Compra

db = SessionLocal()
compras = db.query(Compra).all()

print('=== ESTADOS EN LA BASE DE DATOS ===')
print(f'Total de compras: {len(compras)}\n')

# Mostrar todos los estados
estados_unicos = set()
for compra in compras:
    estado = compra.estado
    estado_str = str(estado)
    estados_unicos.add(estado_str)
    print(f'ID: {compra.id}, Estado: {repr(estado)} (tipo: {type(estado).__name__})')

print(f'\n=== ESTADOS ÚNICOS ENCONTRADOS ===')
for estado in sorted(estados_unicos):
    print(f'  - "{estado}"')

db.close()
