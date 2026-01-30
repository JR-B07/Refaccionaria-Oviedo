# scripts/crear_usuario_inicial.py
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.crud.usuario import usuario_crud
from app.schemas.usuario import UsuarioCreate, RolUsuario

def crear_usuario_inicial():
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el usuario admin
        admin = usuario_crud.obtener_por_nombre_usuario(db, "admin")
        
        if not admin:
            # Crear usuario administrador inicial
            usuario_admin = UsuarioCreate(
                nombre="Administrador",
                apellido_paterno="Sistema",
                email="admin@refaccionaria.com",
                nombre_usuario="admin",
                clave_acceso="Admin123!",  # Cambiar en producción
                rol=RolUsuario.ADMINISTRADOR,
                local_id=1
            )
            
            usuario_crud.crear(db, usuario_admin)
            print("✅ Usuario administrador creado exitosamente")
            print(f"   Usuario: admin")
            print(f"   Contraseña: Admin123!")
            print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
        else:
            print("⚠️  El usuario administrador ya existe")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_inicial()