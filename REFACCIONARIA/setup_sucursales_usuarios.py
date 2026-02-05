#!/usr/bin/env python
"""Script para crear sucursales y usuarios para cada una"""

import hashlib
from app.core.database import SessionLocal
from app.models.usuario import Usuario, RolUsuario, EstadoUsuario
from app.models.local import Local

def crear_sucursales_y_usuarios():
    db = SessionLocal()
    
    print("=" * 70)
    print("CREANDO SUCURSALES Y USUARIOS")
    print("=" * 70)
    
    # Crear Sucursal 1 (Refaccionaria Oviedo)
    sucursal1_exist = db.query(Local).filter_by(nombre="Refaccionaria Oviedo").first()
    if not sucursal1_exist:
        sucursal1 = Local(
            nombre="Refaccionaria Oviedo",
            direccion="Ubicación Principal",
            telefono="555-1001",
            email="sucursal1@refaccionaria.com"
        )
        db.add(sucursal1)
        db.flush()  # Para obtener el ID
        print(f"✅ Sucursal 1 creada: Refaccionaria Oviedo (ID: {sucursal1.id})")
    else:
        sucursal1 = sucursal1_exist
        print(f"ℹ️  Sucursal 1 ya existe: Refaccionaria Oviedo (ID: {sucursal1.id})")
    
    # Crear Sucursal 2 (Filtros y Lubricantes)
    sucursal2_exist = db.query(Local).filter_by(nombre="Filtros y Lubricantes").first()
    if not sucursal2_exist:
        sucursal2 = Local(
            nombre="Filtros y Lubricantes",
            direccion="Ubicación Secundaria",
            telefono="555-1002",
            email="sucursal2@refaccionaria.com"
        )
        db.add(sucursal2)
        db.flush()  # Para obtener el ID
        print(f"✅ Sucursal 2 creada: Filtros y Lubricantes (ID: {sucursal2.id})")
    else:
        sucursal2 = sucursal2_exist
        print(f"ℹ️  Sucursal 2 ya existe: Filtros y Lubricantes (ID: {sucursal2.id})")
    
    db.commit()
    
    print("\n" + "=" * 70)
    print("CREANDO USUARIOS PARA SUCURSALES")
    print("=" * 70)
    
    # Crear usuario para Sucursal 1
    usuario_s1 = db.query(Usuario).filter_by(nombre_usuario="sucursal1").first()
    if not usuario_s1:
        usuario_s1 = Usuario(
            nombre="Gerente",
            apellido_paterno="Sucursal",
            apellido_materno="Uno",
            email="gerente1@refaccionaria.com",
            telefono="555-2001",
            nombre_usuario="sucursal1",
            clave_hash=hashlib.sha256("sucursal1".encode()).hexdigest(),
            rol=RolUsuario.GERENTE,
            estado=EstadoUsuario.ACTIVO,
            local_id=sucursal1.id,
            debe_cambiar_clave=False
        )
        db.add(usuario_s1)
        print(f"✅ Usuario creado: sucursal1 (Gerente de Refaccionaria Oviedo)")
        print(f"   📧 Email: gerente1@refaccionaria.com")
        print(f"   🔑 Password: sucursal1")
    else:
        print(f"ℹ️  Usuario 'sucursal1' ya existe")
    
    # Crear usuario para Sucursal 2
    usuario_s2 = db.query(Usuario).filter_by(nombre_usuario="sucursal2").first()
    if not usuario_s2:
        usuario_s2 = Usuario(
            nombre="Gerente",
            apellido_paterno="Sucursal",
            apellido_materno="Dos",
            email="gerente2@refaccionaria.com",
            telefono="555-2002",
            nombre_usuario="sucursal2",
            clave_hash=hashlib.sha256("sucursal2".encode()).hexdigest(),
            rol=RolUsuario.GERENTE,
            estado=EstadoUsuario.ACTIVO,
            local_id=sucursal2.id,
            debe_cambiar_clave=False
        )
        db.add(usuario_s2)
        print(f"✅ Usuario creado: sucursal2 (Gerente de Filtros y Lubricantes)")
        print(f"   📧 Email: gerente2@refaccionaria.com")
        print(f"   🔑 Password: sucursal2")
    else:
        print(f"ℹ️  Usuario 'sucursal2' ya existe")
    
    db.commit()
    
    # Mostrar resumen final
    print("\n" + "=" * 70)
    print("RESUMEN FINAL - TODOS LOS USUARIOS")
    print("=" * 70)
    
    usuarios = db.query(Usuario).all()
    for u in usuarios:
        local_nombre = "Sin asignar"
        if u.local_id:
            local = db.query(Local).filter_by(id=u.local_id).first()
            if local:
                local_nombre = local.nombre
        print(f"👤 {u.nombre_usuario:15} | Rol: {u.rol.value:15} | Sucursal: {local_nombre}")
    
    print("\n" + "=" * 70)
    print("SUCURSALES DISPONIBLES")
    print("=" * 70)
    locales = db.query(Local).all()
    for loc in locales:
        print(f"🏢 ID {loc.id}: {loc.nombre:30} | {loc.direccion}")
    
    print("\n✅ Configuración completada")
    
    db.close()

if __name__ == "__main__":
    crear_sucursales_y_usuarios()
