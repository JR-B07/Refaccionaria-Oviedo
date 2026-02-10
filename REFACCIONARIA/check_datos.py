#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    from sqlalchemy import create_engine, text
    from app.core.config import settings
    
    engine = create_engine(settings.DATABASE_URL, echo=False)
    
    with engine.connect() as conn:
        print('=== LOCALES ===')
        try:
            result = conn.execute(text('SELECT id, nombre, direccion FROM locales ORDER BY id'))
            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(f'ID: {row[0]}, Nombre: {row[1]}, Dirección: {row[2]}')
            else:
                print('No hay locales')
        except Exception as e:
            print(f'Error: {e}')
        
        print('\n=== PROVEEDORES ===')
        try:
            result = conn.execute(text('SELECT id, clave, nombre FROM proveedores ORDER BY id'))
            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(f'ID: {row[0]}, Clave: {row[1]}, Nombre: {row[2]}')
            else:
                print('No hay proveedores')
        except Exception as e:
            print(f'Error: {e}')
    
except Exception as e:
    print(f'Error: {type(e).__name__}: {str(e)}')
    import traceback
    traceback.print_exc()
