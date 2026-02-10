import sys
sys.path.insert(0, '.')
from app.core.database import SessionLocal
from app.models.cierre_caja import CierreCaja
from app.models.usuario import Usuario
from datetime import datetime

db = SessionLocal()

# Contar cierres totales
total = db.query(CierreCaja).count()
print(f'✅ Total de cierres en la BD: {total}')

# Ver ultimos 5 cierres
print('\n📋 Últimos 5 cierres:')
cierres = db.query(CierreCaja).order_by(CierreCaja.fecha_creacion.desc()).limit(5).all()
for c in cierres:
    usuario = db.query(Usuario).filter(Usuario.id == c.usuario_id).first()
    print(f'   - Caja: {c.caja}, Vendedor: {usuario.nombre if usuario else "N/A"}, Local: {c.local_id}, Fecha: {c.fecha_creacion}')

# Ver cierres del 5 de febrero
from datetime import datetime
fecha_inicio = datetime(2026, 2, 5, 0, 0, 0)
fecha_fin = datetime(2026, 2, 5, 23, 59, 59)
cierres_hoy = db.query(CierreCaja).filter(CierreCaja.fecha_creacion >= fecha_inicio).filter(CierreCaja.fecha_creacion <= fecha_fin).all()
print(f'\n🔍 Cierres del 5/2/2026: {len(cierres_hoy)}')
for c in cierres_hoy:
    usuario = db.query(Usuario).filter(Usuario.id == c.usuario_id).first()
    print(f'   - Caja: {c.caja}, Vendedor: {usuario.nombre if usuario else "N/A"}, Local: {c.local_id}')

db.close()
