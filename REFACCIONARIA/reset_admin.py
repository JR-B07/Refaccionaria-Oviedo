from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import get_password_hash

db = SessionLocal()
try:
    admin = db.query(Usuario).filter(Usuario.nombre_usuario == 'admin').first()
    if admin:
        admin.clave_hash = get_password_hash('admin')
        admin.intentos_fallidos = 0
        db.commit()
        print('✅ Contraseña de admin reseteada a: admin')
        print(f'   Usuario: {admin.nombre_usuario}')
        print(f'   Estado: {admin.estado}')
    else:
        print('❌ Usuario admin no encontrado')
finally:
    db.close()
