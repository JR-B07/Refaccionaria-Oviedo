"""Script para crear todas las tablas en la base de datos."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
# Importar todos los modelos para que se registren en Base.metadata
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.venta import Venta
# Importar modelos adicionales si existen
try:
    from app.models.base import Local
except ImportError:
    pass

print('Creando tablas en la base de datos...')
try:
    Base.metadata.create_all(bind=engine)
    print('✅ Tablas creadas exitosamente')
except Exception as e:
    print(f'❌ Error al crear tablas: {e}')
    import traceback
    traceback.print_exc()
