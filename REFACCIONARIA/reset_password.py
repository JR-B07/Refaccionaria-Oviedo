#!/usr/bin/env python
# Script para resetear la contraseña del admin
import sys
from pathlib import Path
import hashlib

sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.crud.usuario import usuario_crud

db = SessionLocal()

try:
    # Obtener el usuario admin
    admin = usuario_crud.obtener_por_nombre_usuario(db, "admin")
    
    if admin:
        # Usar un hash simple SHA256 para esta contraseña
        password = "Admin123!"
        admin.clave_hash = hashlib.sha256(password.encode()).hexdigest()
        db.commit()
        print("✅ Contraseña del usuario admin restablecida exitosamente")
        print("   Usuario: admin")
        print("   Contraseña: Admin123!")
    else:
        print("❌ Usuario admin no encontrado")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
