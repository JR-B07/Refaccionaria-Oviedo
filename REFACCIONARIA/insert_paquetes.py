#!/usr/bin/env python3
"""Insertar paquetes de ejemplo en la BD"""
import sys
sys.path.insert(0, 'c:\\Users\\india\\Desktop\\REFACCIONARIA')

if __name__ == '__main__':
    from datetime import datetime
    from app.core.database import SessionLocal
    from app.models.paquete import Paquete
    
    db = SessionLocal()
    
    try:
        # Limpiar paquetes previos
        db.query(Paquete).delete()
        
        # Crear paquetes
        p1 = Paquete(
            nombre='Kit Suspensión Delantera',
            clase='Suspensión',
            descripcion='Kit completo de suspensión delantera con amortiguadores y resortes',
            activo=True
        )
        
        p2 = Paquete(
            nombre='Kit Frenos Completo',
            clase='Frenos',
            descripcion='Sistema de frenos completo con pastillas, discos y mangueras',
            activo=True
        )
        
        db.add(p1)
        db.add(p2)
        db.commit()
        
        print('✅ Paquetes insertados:')
        paquetes = db.query(Paquete).all()
        for p in paquetes:
            print(f'   - {p.id}: {p.nombre}')
            
    except Exception as e:
        print(f'❌ Error: {e}')
        db.rollback()
    finally:
        db.close()
