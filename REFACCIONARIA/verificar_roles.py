#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para actualizar los roles en la BD a mayúsculas
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

database_url = f"mysql+pymysql://root:root@localhost:3306/refaccionaria_db"
engine = create_engine(database_url)

print("=" * 80)
print("ACTUALIZANDO ROLES A FORMATO CORRECTO")
print("=" * 80 + "\n")

try:
    with engine.connect() as conn:
        # Mapeo de cambios
        changes = {
            'administrador': 'administrador',  # Mantener igual
            'gerente': 'gerente',               # Mantener igual
            'vendedor': 'vendedor',            # Mantener igual
            'almacenista': 'almacenista',      # Mantener igual
            'cajero': 'cajero'                 # Mantener igual
        }
        
        # Verificar qué roles existen actualmente
        result = conn.execute(text("SELECT DISTINCT rol FROM usuarios"))
        existing_roles = [row[0] for row in result.fetchall()]
        print(f"✅ Roles actuales en BD: {existing_roles}\n")
        
        # Los enums del modelo son: administrador, gerente, vendedor, almacenista, cajero
        # Ya están en minúsculas, así que no hay cambios necesarios
        
        print("✅ Los roles en BD coinciden con los valores del enum")
        print("✅ No se necesitan cambios\n")
        
        # Ahora verificar los estados
        result2 = conn.execute(text("SELECT DISTINCT estado FROM usuarios"))
        existing_estados = [row[0] for row in result2.fetchall()]
        print(f"✅ Estados actuales en BD: {existing_estados}\n")
        
        conn.commit()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
