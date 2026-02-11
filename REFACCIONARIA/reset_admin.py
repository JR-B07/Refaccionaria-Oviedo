from app.core.database import SessionLocal
from app.models.usuario import Usuario, RolUsuario, EstadoUsuario
import hashlib
import secrets

db = SessionLocal()
try:
    admin = db.query(Usuario).filter(Usuario.nombre_usuario == 'admin').first()
    sucursal1 = db.query(Usuario).filter(Usuario.nombre_usuario == 'sucursal1').first()
    sucursal2 = db.query(Usuario).filter(Usuario.nombre_usuario == 'sucursal2').first()

    if admin:
        admin.clave_hash = hashlib.sha256("admin".encode()).hexdigest()
        admin.intentos_fallidos = 0
        admin.debe_cambiar_clave = False
    else:
        admin = Usuario(
            nombre="Administrador",
            apellido_paterno="",
            apellido_materno="",
            email="admin@refaccionaria.local",
            telefono="",
            nombre_usuario="admin",
            clave_hash=hashlib.sha256("admin".encode()).hexdigest(),
            rol=RolUsuario.ADMINISTRADOR,
            estado=EstadoUsuario.ACTIVO,
            local_id=None,
            debe_cambiar_clave=False,
        )
        db.add(admin)

    if sucursal1:
        sucursal1.clave_hash = hashlib.sha256("sucursal1".encode()).hexdigest()
        sucursal1.intentos_fallidos = 0
        sucursal1.debe_cambiar_clave = False
    else:
        sucursal1 = Usuario(
            nombre="Sucursal1",
            apellido_paterno="",
            apellido_materno="",
            email="sucursal1@refaccionaria.local",
            telefono="",
            nombre_usuario="sucursal1",
            clave_hash=hashlib.sha256("sucursal1".encode()).hexdigest(),
            rol=RolUsuario.GERENTE,
            estado=EstadoUsuario.ACTIVO,
            local_id=1,
            debe_cambiar_clave=False,
        )
        db.add(sucursal1)

    if sucursal2:
        sucursal2.clave_hash = hashlib.sha256("sucursal2".encode()).hexdigest()
        sucursal2.intentos_fallidos = 0
        sucursal2.debe_cambiar_clave = False
    else:
        sucursal2 = Usuario(
            nombre="Sucursal2",
            apellido_paterno="",
            apellido_materno="",
            email="sucursal2@refaccionaria.local",
            telefono="",
            nombre_usuario="sucursal2",
            clave_hash=hashlib.sha256("sucursal2".encode()).hexdigest(),
            rol=RolUsuario.GERENTE,
            estado=EstadoUsuario.ACTIVO,
            local_id=3,
            debe_cambiar_clave=False,
        )
        db.add(sucursal2)

    desactivados = 0
    usuarios_otros = (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario.notin_(["admin", "sucursal1", "sucursal2"]))
        .all()
    )

    for usuario in usuarios_otros:
        usuario.estado = EstadoUsuario.INACTIVO
        usuario.debe_cambiar_clave = True
        usuario.intentos_fallidos = 0
        usuario.clave_hash = hashlib.sha256(secrets.token_hex(16).encode()).hexdigest()
        usuario.nombre_usuario = f"disabled_{usuario.id}"
        usuario.email = f"disabled_{usuario.id}@refaccionaria.local"
        desactivados += 1

    db.commit()
    print("✅ Se mantuvieron los usuarios admin, sucursal1 y sucursal2")
    print("   Usuario: admin / Contraseña: admin")
    print("   Usuario: sucursal1 / Contraseña: sucursal1")
    print("   Usuario: sucursal2 / Contraseña: sucursal2")
    print(f"   Usuarios desactivados: {desactivados}")
finally:
    db.close()
