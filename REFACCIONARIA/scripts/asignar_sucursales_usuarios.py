# scripts/asignar_sucursales_usuarios.py
"""
Script para asignar sucursales a usuarios existentes
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.local import Local

def asignar_sucursales():
    """Asignar sucursales a usuarios existentes"""
    
    db = SessionLocal()
    
    try:
        # Obtener todas las sucursales
        sucursales = db.query(Local).all()
        
        if not sucursales:
            print("✗ No hay sucursales en el sistema. Ejecuta primero crear_sucursales.py")
            return
        
        print(f"Sucursales disponibles:")
        for s in sucursales:
            print(f"  {s.id}. {s.nombre}")
        
        # Obtener todos los usuarios
        usuarios = db.query(Usuario).all()
        
        if not usuarios:
            print("✗ No hay usuarios en el sistema")
            return
        
        print(f"\n✓ Encontrados {len(usuarios)} usuarios")
        
        # Asignar sucursal por defecto (sucursal 1) a usuarios sin sucursal
        sucursal_principal = sucursales[0]
        usuarios_actualizados = 0
        
        for usuario in usuarios:
            if not usuario.local_id:
                usuario.local_id = sucursal_principal.id
                usuarios_actualizados += 1
                print(f"  - {usuario.nombre_usuario} → {sucursal_principal.nombre}")
        
        if usuarios_actualizados > 0:
            db.commit()
            print(f"\n✓ {usuarios_actualizados} usuarios asignados a {sucursal_principal.nombre}")
        else:
            print("\n✓ Todos los usuarios ya tienen sucursal asignada")
        
        # Mostrar resumen
        print("\n=== Resumen de usuarios por sucursal ===")
        for sucursal in sucursales:
            count = db.query(Usuario).filter(Usuario.local_id == sucursal.id).count()
            print(f"  {sucursal.nombre}: {count} usuario(s)")
        
    except Exception as e:
        print(f"✗ Error al asignar sucursales: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Asignación de Sucursales a Usuarios ===")
    asignar_sucursales()
    print("=== Proceso completado ===")
