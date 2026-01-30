#!/usr/bin/env python
# Script para crear tabla retiros_caja e insertar datos de ejemplo

from app.core.database import SessionLocal, engine
from app.models.base import ModeloBase
from app.models.retiro_caja import RetiroCaja
from app.models.usuario import Usuario
from app.models.local import Local

def crear_tabla_retiros():
    print("="*60)
    print("📦 CREANDO TABLA RETIROS_CAJA")
    print("="*60)
    
    try:
        # Crear todas las tablas (incluida retiros_caja)
        ModeloBase.metadata.create_all(bind=engine)
        print("✅ Tabla retiros_caja creada exitosamente")
        
        # Verificar si ya hay datos
        session = SessionLocal()
        count = session.query(RetiroCaja).count()
        
        if count > 0:
            print(f"⚠️ Ya existen {count} retiros en la base de datos")
            print("No se insertarán datos de ejemplo")
        else:
            print("📝 Insertando datos de ejemplo...")
            
            # Datos de ejemplo
            retiros_ejemplo = [
                {
                    'folio': 'R-20260120-001',
                    'local_id': 1,
                    'usuario_id': 3,
                    'monto': 4800.00,
                    'descripcion': 'RETIRO GENERADO AUTOMATICO'
                },
                {
                    'folio': 'R-20260119-002',
                    'local_id': 1,
                    'usuario_id': 3,
                    'monto': 5100.00,
                    'descripcion': 'RETIRO GENERADO AUTOMATICO'
                },
                {
                    'folio': 'R-20260117-003',
                    'local_id': 1,
                    'usuario_id': 3,
                    'monto': 4800.00,
                    'descripcion': 'RETIRO GENERADO AUTOMATICO'
                },
                {
                    'folio': 'R-20260115-004',
                    'local_id': 2,
                    'usuario_id': 7,  # Maria
                    'monto': 3500.00,
                    'descripcion': 'RETIRO GENERADO AUTOMATICO'
                },
                {
                    'folio': 'R-20260114-005',
                    'local_id': 2,
                    'usuario_id': 7,
                    'monto': 2800.00,
                    'descripcion': 'COMPRA ACEITE FRAM'
                }
            ]
            
            for retiro_data in retiros_ejemplo:
                retiro = RetiroCaja(**retiro_data)
                session.add(retiro)
            
            session.commit()
            print(f"✅ {len(retiros_ejemplo)} retiros de ejemplo insertados")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("📊 RESUMEN DE RETIROS POR SUCURSAL")
        print("="*60)
        
        retiros = session.query(
            Local.nombre,
            RetiroCaja.folio,
            RetiroCaja.monto,
            RetiroCaja.descripcion,
            Usuario.nombre.label('usuario')
        ).join(Local, RetiroCaja.local_id == Local.id)\
         .join(Usuario, RetiroCaja.usuario_id == Usuario.id)\
         .order_by(RetiroCaja.fecha_retiro.desc())\
         .limit(10).all()
        
        for r in retiros:
            print(f"🏪 {r.nombre:25} | {r.folio:18} | ${r.monto:8.2f} | {r.usuario:15} | {r.descripcion[:30]}")
        
        print("\n✅ Sistema de retiros de caja listo para usar")
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_tabla_retiros()
