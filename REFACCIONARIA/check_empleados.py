#!/usr/bin/env python3
"""
Script para verificar si existen empleados en la base de datos
"""
import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.empleado import Empleado

def check_empleados():
    db = SessionLocal()
    try:
        # Contar empleados
        total = db.query(Empleado).count()
        print(f"\n📊 Total de empleados en BD: {total}")
        
        if total > 0:
            # Mostrar algunos empleados
            empleados = db.query(Empleado).limit(10).all()
            print("\n👥 Primeros empleados:")
            print("-" * 80)
            for emp in empleados:
                estado = "✅ Activo" if emp.activo else "❌ Inactivo"
                print(f"ID: {emp.id:3d} | {emp.nombre:30s} | {emp.puesto:20s} | {estado}")
            
            if total > 10:
                print(f"\n... y {total - 10} más")
        else:
            print("\n⚠️  No hay empleados registrados en la base de datos")
            
    except Exception as e:
        print(f"\n❌ Error al consultar empleados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_empleados()
