#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para insertar datos de ejemplo en la tabla de empleados
"""

import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.empleado import Empleado
from datetime import date

# Datos de ejemplo obtenidos del HTML
EMPLEADOS_EJEMPLO = [
    {
        'nombre': 'JUAN CARLOS GARCÍA',
        'puesto': 'GERENTE GENERAL',
        'departamento': 'ADMINISTRACIÓN',
        'sucursal': 'MATRIZ',
        'organizacion': 'REFACCIONARIA OVIEDO',
        'fecha_alta': date(2015, 3, 15),
        'activo': True,
        'notas': 'Empleado activo'
    },
    {
        'nombre': 'MARÍA RODRÍGUEZ',
        'puesto': 'VENDEDOR',
        'departamento': 'VENTAS',
        'sucursal': 'MATRIZ',
        'organizacion': 'REFACCIONARIA OVIEDO',
        'fecha_alta': date(2018, 7, 22),
        'activo': True,
        'notas': 'Vendedor senior'
    },
    {
        'nombre': 'LUIS MARTÍNEZ',
        'puesto': 'ALMACENISTA',
        'departamento': 'LOGÍSTICA',
        'sucursal': 'CEDIS',
        'organizacion': 'REFACCIONARIA OVIEDO',
        'fecha_alta': date(2019, 1, 10),
        'activo': True,
        'notas': 'Responsable del almacén'
    },
    {
        'nombre': 'SANDRA TORRES',
        'puesto': 'CAJERO',
        'departamento': 'TESORERÍA',
        'sucursal': 'MATRIZ',
        'organizacion': 'REFACCIONARIA OVIEDO',
        'fecha_alta': date(2020, 5, 3),
        'activo': True,
        'notas': 'Manejo de caja'
    },
    {
        'nombre': 'CARLOS HERNÁNDEZ',
        'puesto': 'REPARTIDOR',
        'departamento': 'LOGÍSTICA',
        'sucursal': 'CEDIS',
        'organizacion': 'REFACCIONARIA OVIEDO',
        'fecha_alta': date(2020, 11, 2),
        'activo': False,
        'fecha_baja': date(2024, 1, 10),
        'notas': 'Baja voluntaria'
    },
    {
        'nombre': 'ALFREDO PEREZ',
        'puesto': 'REPARTIDOR',
        'departamento': 'LOGISTICA',
        'sucursal': 'CEDIS',
        'organizacion': 'REFACCIONARIA OVIEDO',
        'fecha_alta': date(2020, 11, 2),
        'fecha_baja': date(2024, 1, 10),
        'activo': False,
        'notas': 'Baja voluntaria'
    },
]


def insertar_empleados_ejemplo():
    """Inserta empleados de ejemplo en la BD"""
    print("=" * 70)
    print("INSERTAR EMPLEADOS DE EJEMPLO")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        # Verificar si ya existen empleados
        count = db.query(Empleado).count()
        
        if count > 0:
            print(f"\n⚠️  Ya existen {count} empleados en la BD")
            respuesta = input("¿Deseas insertar más empleados? (s/n): ").lower()
            if respuesta != 's':
                print("Operación cancelada")
                return
        
        # Insertar empleados
        print(f"\n📝 Insertando {len(EMPLEADOS_EJEMPLO)} empleados de ejemplo...\n")
        
        for emp_data in EMPLEADOS_EJEMPLO:
            # Crear objeto Empleado
            empleado = Empleado(**emp_data)
            db.add(empleado)
            print(f"  ✓ {emp_data['nombre']} - {emp_data['puesto']}")
        
        # Commit
        db.commit()
        print(f"\n✅ {len(EMPLEADOS_EJEMPLO)} empleados insertados correctamente")
        
        # Verificar
        total = db.query(Empleado).count()
        print(f"📊 Total de empleados en BD: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al insertar empleados: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
    
    return True


if __name__ == "__main__":
    success = insertar_empleados_ejemplo()
    sys.exit(0 if success else 1)
