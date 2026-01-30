# scripts/crear_sucursales.py
"""
Script para crear las dos sucursales iniciales del sistema
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.local import Local
from app.models.base import ModeloBase

def crear_sucursales():
    """Crear las dos sucursales del sistema"""
    
    # Crear tablas si no existen
    ModeloBase.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existen sucursales
        sucursales_existentes = db.query(Local).count()
        
        if sucursales_existentes > 0:
            print(f"✓ Ya existen {sucursales_existentes} sucursal(es) en el sistema")
            sucursales = db.query(Local).all()
            for s in sucursales:
                print(f"  - ID: {s.id}, Nombre: {s.nombre}")
            return
        
        # Crear Sucursal 1
        sucursal1 = Local(
            nombre="Sucursal Principal",
            direccion="Dirección Sucursal 1",
            telefono="555-0001",
            email="sucursal1@refaccionaria.com"
        )
        
        # Crear Sucursal 2
        sucursal2 = Local(
            nombre="Sucursal 2",
            direccion="Dirección Sucursal 2",
            telefono="555-0002",
            email="sucursal2@refaccionaria.com"
        )
        
        db.add(sucursal1)
        db.add(sucursal2)
        db.commit()
        
        print("✓ Sucursales creadas exitosamente:")
        print(f"  - {sucursal1.nombre} (ID: {sucursal1.id})")
        print(f"  - {sucursal2.nombre} (ID: {sucursal2.id})")
        
    except Exception as e:
        print(f"✗ Error al crear sucursales: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Creación de Sucursales ===")
    crear_sucursales()
    print("=== Proceso completado ===")
