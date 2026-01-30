#!/usr/bin/env python
# Script para crear usuarios para sucursal 2

import hashlib
from datetime import datetime
from app.core.database import SessionLocal
from app.models.usuario import Usuario, RolUsuario, EstadoUsuario

def crear_usuarios_sucursal2():
    session = SessionLocal()
    
    # Verificar si ya existen
    maria = session.query(Usuario).filter_by(nombre_usuario="maria").first()
    carlos = session.query(Usuario).filter_by(nombre_usuario="carlos").first()
    
    if not maria:
        # Crear usuario para sucursal 2 (REFACCIONARIA OVIEDO)
        usuario_sucursal2 = Usuario(
            nombre="María",
            apellido_paterno="García",
            apellido_materno="López",
            email="maria@refac.com",
            telefono="555-0001",
            nombre_usuario="maria",
            clave_hash=hashlib.sha256("password123".encode()).hexdigest(),
            rol=RolUsuario.VENDEDOR,
            estado=EstadoUsuario.ACTIVO,
            local_id=2,  # Sucursal REFACCIONARIA OVIEDO
            debe_cambiar_clave=False
        )
        session.add(usuario_sucursal2)
        print("✅ Usuario María (vendedor) creado para sucursal 2")
    else:
        print("⚠️ Usuario María ya existe")
    
    if not carlos:
        # Crear usuario gerente para sucursal 2
        usuario_gerente2 = Usuario(
            nombre="Carlos",
            apellido_paterno="Mendez",
            apellido_materno="Rodriguez",
            email="carlos@refac.com",
            telefono="555-0002",
            nombre_usuario="carlos",
            clave_hash=hashlib.sha256("password123".encode()).hexdigest(),
            rol=RolUsuario.GERENTE,
            estado=EstadoUsuario.ACTIVO,
            local_id=2,  # Sucursal REFACCIONARIA OVIEDO
            debe_cambiar_clave=False
        )
        session.add(usuario_gerente2)
        print("✅ Usuario Carlos (gerente) creado para sucursal 2")
    else:
        print("⚠️ Usuario Carlos ya existe")
    
    session.commit()
    print("\n✅ Base de datos actualizada")
    
    # Mostrar todos los usuarios
    print("\n" + "="*60)
    print("📋 USUARIOS EN EL SISTEMA")
    print("="*60)
    usuarios = session.query(Usuario).all()
    for u in usuarios:
        local_name = "REFACCIONARIA OVIEDO" if u.local_id == 2 else "Local Principal" if u.local_id == 1 else "Desconocido"
        print(f"👤 {u.nombre_usuario:15} | {u.nombre:20} | Sucursal: {local_name}")
    
    session.close()

if __name__ == "__main__":
    crear_usuarios_sucursal2()
