# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Motor de conexión para MySQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexión antes de usarla
    pool_recycle=3600,   # Recicla conexiones cada hora
    pool_size=10,        # Tamaño del pool
    max_overflow=20,     # Conexiones extra si se necesitan
    echo=settings.DEBUG  # Muestra queries en desarrollo
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Importar todos los modelos para registrarlos en la Base
# Esta importación es necesaria para que SQLAlchemy reconozca las relaciones
from app.models.local import Local  # noqa: F401, E402
from app.models.usuario import Usuario  # noqa: F401, E402
from app.models.producto import Producto  # noqa: F401, E402
from app.models.cliente import Cliente  # noqa: F401, E402
from app.models.venta import Venta  # noqa: F401, E402
from app.models.proveedor import Proveedor  # noqa: F401, E402
from app.models.vale_venta import ValeVenta  # noqa: F401, E402
from app.models.traspaso import Traspaso, DetalleTraspaso  # noqa: F401, E402
from app.models.compra import Compra, DetalleCompra  # noqa: F401, E402
from app.models.marca import Marca  # noqa: F401, E402
from app.models.cierre_caja import CierreCaja  # noqa: F401, E402
from app.models.paquete import Paquete, PaqueteProducto  # noqa: F401, E402
from app.models.grupo import Grupo  # noqa: F401, E402
from app.models.arqueo_caja import ArqueoCaja  # noqa: F401, E402
from app.models.asistencia import AsistenciaEmpleado  # noqa: F401, E402
from app.models.promocion import Promocion  # noqa: F401, E402

# Dependencia para obtener sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()