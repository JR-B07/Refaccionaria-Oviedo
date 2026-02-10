#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    from sqlalchemy import create_engine, text
    from app.core.config import settings
    
    engine = create_engine(settings.DATABASE_URL, echo=False)
    with engine.connect() as conn:
        print("=== USUARIOS ===")
        result = conn.execute(text('SELECT id, nombre_usuario, estado FROM usuarios LIMIT 10'))
        for row in result:
            print(f"ID: {row[0]}, Usuario: {row[1]}, Estado: {row[2]}")
        
        print("\n=== VALES_VENTA ===")
        result = conn.execute(text('SELECT id, folio, tipo FROM vales_venta LIMIT 10'))
        for row in result:
            print(f"ID: {row[0]}, Folio: {row[1]}, Tipo: {row[2]}")
            
except Exception as e:
    print(f'Error: {type(e).__name__}: {str(e)}')
    import traceback
    traceback.print_exc()
