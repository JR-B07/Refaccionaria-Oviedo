#!/usr/bin/env python
"""Script para verificar usuarios y sucursales"""

from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.local import Local

def main():
    db = SessionLocal()
    
    print("=" * 70)
    print("USUARIOS EN EL SISTEMA")
    print("=" * 70)
    usuarios = db.query(Usuario).all()
    if usuarios:
        for u in usuarios:
            print(f"ID: {u.id:3} | Usuario: {u.nombre_usuario:15} | Rol: {u.rol:15} | Local ID: {u.local_id}")
    else:
        print("No hay usuarios en la base de datos")
    
    print("\n" + "=" * 70)
    print("SUCURSALES (LOCALES) EN EL SISTEMA")
    print("=" * 70)
    locales = db.query(Local).all()
    if locales:
        for loc in locales:
            print(f"ID: {loc.id:3} | Nombre: {loc.nombre:30} | Dirección: {loc.direccion}")
    else:
        print("No hay locales/sucursales en la base de datos")
    
    db.close()

if __name__ == "__main__":
    main()
