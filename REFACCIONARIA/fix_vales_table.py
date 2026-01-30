from app.core.database import engine
from sqlalchemy import text, inspect

# Verificar si la columna fecha_uso existe
inspector = inspect(engine)
columns = [col['name'] for col in inspector.get_columns('vales_venta')]

print("Columnas actuales en vales_venta:", columns)

if 'fecha_uso' not in columns:
    print("Agregando columna fecha_uso...")
    with engine.connect() as conn:
        conn.execute(text('ALTER TABLE vales_venta ADD COLUMN fecha_uso DATETIME NULL AFTER usado'))
        conn.commit()
    print("✅ Columna fecha_uso agregada")
else:
    print("✅ Columna fecha_uso ya existe")

# Verificar nuevamente
columns = [col['name'] for col in inspector.get_columns('vales_venta')]
print("Columnas finales:", columns)
