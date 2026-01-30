"""
Script para agregar marcas de ejemplo
"""
import sys
sys.path.insert(0, '/Users/india/Desktop/REFACCIONARIA')

from app.core.database import SessionLocal
from app.models.marca import Marca

session = SessionLocal()

try:
    # Verificar si ya existen
    count = session.query(Marca).count()
    print(f'Marcas existentes: {count}')
    
    if count == 0:
        marcas = [
            Marca(nombre='MOOG', pais_origen='USA', activo=1),
            Marca(nombre='BOSCH', pais_origen='Alemania', activo=1),
            Marca(nombre='GATES', pais_origen='USA', activo=1),
            Marca(nombre='ACDelco', pais_origen='USA', activo=1),
        ]
        session.add_all(marcas)
        session.commit()
        print('✓ Marcas de ejemplo agregadas')
    
    # Listar todas
    todas = session.query(Marca).filter(Marca.activo == 1).all()
    print(f'✓ Total de marcas activas: {len(todas)}')
    for m in todas:
        print(f'  - {m.nombre} ({m.pais_origen})')

except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
finally:
    session.close()
