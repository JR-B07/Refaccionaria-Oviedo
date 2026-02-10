import sys
sys.path.insert(0, '.')
from app.core.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
usuarios = db.query(Usuario).all()
print(f'Usuarios en la BD:')
for u in usuarios:
    print(f'  ID: {u.id}, Nombre: {u.nombre}, Usuario: {u.nombre_usuario}')
db.close()
