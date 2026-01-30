"""Script para crear usuarios de prueba en la BD."""
import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.usuario import Usuario, RolUsuario, EstadoUsuario
from app.models.local import Local


def ensure_local(db):
    """Crea el local principal si aún no existe."""
    existing_local = db.query(Local).filter(Local.id == 1).first()
    if existing_local:
        print('✅ Local principal ya existe')
        return existing_local

    local = Local(
        id=1,
        nombre='Local Principal',
        direccion='Calle Principal 123',
        telefono='555-0000',
        email='local@test.com'
    )
    db.add(local)
    db.commit()
    print('✅ Local creado: Local Principal (ID: 1)')
    return local


def ensure_user(db, *, nombre, apellido_paterno=None, apellido_materno=None, email,
                telefono='', nombre_usuario, clave_plana, rol=RolUsuario.VENDEDOR,
                local_id=1):
    """Crea un usuario si no existe, usando contraseñas con bcrypt."""
    existing = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if existing:
        print(f'✅ Usuario {nombre_usuario} ya existe (ID: {existing.id})')
        return existing

    usuario = Usuario(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        email=email,
        telefono=telefono,
        nombre_usuario=nombre_usuario,
        clave_hash=get_password_hash(clave_plana),
        rol=rol,
        estado=EstadoUsuario.ACTIVO,
        local_id=local_id
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    print(f'✅ Usuario creado: {nombre_usuario} (ID: {usuario.id})')
    return usuario


def main():
    print('Creando usuarios de prueba...')
    db = SessionLocal()

    try:
        ensure_local(db)

        ensure_user(
            db,
            nombre='Administrador',
            apellido_paterno='Sistema',
            email='admin@test.com',
            nombre_usuario='admin',
            clave_plana='admin',
            rol=RolUsuario.ADMINISTRADOR
        )

        ensure_user(
            db,
            nombre='Juan',
            apellido_paterno='Perez',
            apellido_materno='Lopez',
            email='vendedor@test.com',
            telefono='555-1234',
            nombre_usuario='vendedor',
            clave_plana='vendedor',
            rol=RolUsuario.VENDEDOR
        )

        ensure_user(
            db,
            nombre='Vendedor 1',
            email='vendedor1@test.com',
            nombre_usuario='vendedor1',
            clave_plana='Vendedor123!',
            rol=RolUsuario.VENDEDOR
        )

        ensure_user(
            db,
            nombre='Vendedor 2',
            email='vendedor2@test.com',
            nombre_usuario='vendedor2',
            clave_plana='Vendedor123!',
            rol=RolUsuario.VENDEDOR
        )

        ensure_user(
            db,
            nombre='Reinaldo',
            apellido_paterno='Oviedo',
            email='reinaldo.oviedo@test.com',
            telefono='555-6789',
            nombre_usuario='reinaldo',
            clave_plana='Reinaldo123!',
            rol=RolUsuario.VENDEDOR
        )

    except Exception as e:
        print(f'❌ Error: {e}')
        traceback.print_exc()
    finally:
        db.close()

    print('\n✅ Usuarios de prueba listos')


if __name__ == "__main__":
    main()
