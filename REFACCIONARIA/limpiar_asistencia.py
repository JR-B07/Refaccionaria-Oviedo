from app.core.database import SessionLocal
from app.models.asistencia import AsistenciaEmpleado

db = SessionLocal()
try:
    count = db.query(AsistenciaEmpleado).count()
    db.query(AsistenciaEmpleado).delete()
    db.commit()
    print(f'✅ Se eliminaron {count} registros de asistencia')
except Exception as e:
    db.rollback()
    print(f'❌ Error: {e}')
finally:
    db.close()
