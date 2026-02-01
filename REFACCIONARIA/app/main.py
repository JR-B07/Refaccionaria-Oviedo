# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

# Intenta importar los módulos, pero continúa si fallan
try:
    from app.api.v1.api import api_router
    from app.core.database import engine, Base
    HAS_DB = True
except ImportError as e:
    print(f"⚠️  Advertencia en imports: {e}")
    HAS_DB = False
    api_router = None

# Permitir evitar la inicialización de la base de datos en entornos de prueba
import os
SKIP_DB_INIT = os.getenv("SKIP_DB_INIT", "0") == "1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=" * 50)
    print("🚀 Sistema de Refaccionaria ERP")
    print(f"📊 Versión: {settings.VERSION}")
    print(f"🔧 Debug: {settings.DEBUG}")
    print(f"🏪 Local ID: {settings.LOCAL_ID}")
    print("=" * 50)
    
    if HAS_DB:
        if SKIP_DB_INIT:
            print("⚠️  SKIP_DB_INIT activo: se omite creación de tablas")
        else:
            try:
                print("📦 Inicializando base de datos...")
                Base.metadata.create_all(bind=engine)
                print("✅ Base de datos lista")
            except Exception as e:
                print(f"❌ Error en DB: {e}")
    else:
        print("⚠️  Modo sin base de datos")
    
    print(f"🌐 Servidor: http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("\n👋 Sistema detenido")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Montar archivos estáticos (CSS, JS, imágenes)
import os
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router si existe
if api_router:
    app.include_router(api_router, prefix=settings.API_V1_STR)

# Endpoints básicos
@app.get("/")
def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if HAS_DB else "not_configured",
        "endpoints": [
            "/health",
            "/docs",
            "/api/v1/auth/login" if api_router else "/api/login"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "refaccionaria-api",
        "timestamp": datetime.utcnow().isoformat()
    }

# Login temporal si no hay módulos cargados
if not api_router:
    @app.post("/api/login")
    def login_temporal(username: str, password: str):
        if username == "admin" and password == "admin123":
            return {
                "success": True,
                "message": "Login exitoso (modo temporal)",
                "user": {
                    "id": 1,
                    "username": "admin",
                    "role": "administrador",
                    "local_id": settings.LOCAL_ID
                }
            }
        return {"success": False, "message": "Credenciales incorrectas"}

@app.get("/login")
def login_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/login.html")

@app.get("/dashboard")
def dashboard_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/dashboard.html")

@app.get("/admin")
def admin_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/admin.html")

@app.get("/cajas")
def cajas_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/cajas.html")

@app.get("/retiros-caja")
def retiros_caja_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/retiros_caja.html")

@app.get("/reportes")
def reportes_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/reportes.html")

@app.get("/gastos")
def gastos_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/gastos.html")

@app.get("/almacen")
def almacen_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/almacen.html")


@app.get("/proveedores")
def proveedores_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/proveedores.html")

@app.get("/proveedor-detalle")
def proveedor_detalle_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/proveedor_detalle.html")

@app.get("/vales-venta")
def vales_venta_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/vales_venta.html")

@app.get("/traspasos")
def traspasos_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/traspasos.html")

@app.get("/productos-servicios")
def productos_servicios_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/productos.html")

@app.get("/busqueda-avanzada-productos")
def busqueda_avanzada_productos_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/busqueda_avanzada_productos.html")

@app.get("/cargar-productos")
def cargar_productos_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/cargar_productos.html")

@app.get("/reporte-compras")
def reporte_compras_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/compras_generales.html")

@app.get("/compras")
def compras_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/compras.html")

@app.get("/recepciones")
def recepciones_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/recepciones.html")

@app.get("/tickets")
def tickets_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/tickets.html")

@app.get("/ventas")
def ventas_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/ventas.html")

@app.get("/devoluciones-venta")
def devoluciones_venta_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/devoluciones.html")

@app.get("/nueva-venta")
def nueva_venta_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/nueva_venta.html")

@app.get("/ventasdetalladas")
def ventasdetalladas_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/ventasdetalladas.html")

@app.get("/reporte-ventas-detalladas")
def reporte_ventas_detalladas_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/ventasdetalladas.html")

@app.get("/rrhh")
def rrhh_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/rrhh.html")

@app.get("/registros-asistencia")
def registros_asistencia_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/registros_asistencia.html")

@app.get("/reporte-devoluciones")
def reporte_devoluciones_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/devolucionesdetalladas.html")

@app.get("/cajas-cierre")
def cajas_cierre_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/cajas_cierre.html")

@app.get("/reporte-grafica-ventas")
def reporte_grafica_ventas_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/grafica_ventas.html")

@app.get("/paquetes")
def paquetes_page():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/paquetes.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)