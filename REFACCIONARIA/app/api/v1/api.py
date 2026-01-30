"""Router central para la API v1.

Incluye routers de los submódulos de `app.api.v1.endpoints` si existen.
"""

from fastapi import APIRouter

api_router = APIRouter()

# Intentar incluir routers disponibles bajo app.api.v1.endpoints
try:
    from app.api.v1.endpoints import auth as auth_module
    api_router.include_router(auth_module.router, prefix="/auth", tags=["Autenticación"])
except Exception as e:
    print("⚠️  Módulo auth no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import usuarios as usuarios_module
    api_router.include_router(usuarios_module.router, prefix="/usuarios", tags=["Usuarios"])
except Exception:
    # No hay módulo usuarios; seguir sin él
    pass

try:
    from app.api.v1.endpoints import clientes as clientes_module
    api_router.include_router(clientes_module.router, tags=["Clientes"])
except Exception as e:
    print("⚠️  Módulo clientes no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import reportes as reportes_module
    api_router.include_router(reportes_module.router, tags=["Reportes"])
except Exception as e:
    print("⚠️  Módulo reportes no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import proveedores as proveedores_module
    api_router.include_router(proveedores_module.router, tags=["Proveedores"])
except Exception as e:
    print("⚠️  Módulo proveedores no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import vales_venta as vales_venta_module
    api_router.include_router(vales_venta_module.router, tags=["Vales de Venta"])
except Exception as e:
    print("⚠️  Módulo vales_venta no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import traspasos as traspasos_module
    api_router.include_router(traspasos_module.router, tags=["Traspasos"])
except Exception as e:
    print("⚠️  Módulo traspasos no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import compras as compras_module
    api_router.include_router(compras_module.router, tags=["Compras"])
except Exception as e:
    print("⚠️  Módulo compras no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import productos as productos_module
    api_router.include_router(productos_module.router, prefix="/productos", tags=["Productos"])
except Exception as e:
    print("⚠️  Módulo productos no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import paquetes as paquetes_module
    api_router.include_router(paquetes_module.router, tags=["Paquetes (Kits)"])
except Exception as e:
    print("⚠️  Módulo paquetes no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import grupos as grupos_module
    api_router.include_router(grupos_module.router, tags=["Grupos"])
except Exception as e:
    print("⚠️  Módulo grupos no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import tickets as tickets_module
    print("[DEBUG] Registrando router de tickets en api_router...")
    api_router.include_router(tickets_module.router, prefix="/tickets", tags=["Tickets"])
    print("[DEBUG] Router de tickets registrado correctamente.")
except Exception as e:
    print("⚠️  Módulo tickets no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import cierres_caja as cierres_caja_module
    api_router.include_router(cierres_caja_module.router)
except Exception as e:
    print("⚠️  Módulo cierres_caja no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import marca as marca_module
    api_router.include_router(marca_module.router, prefix="/marcas", tags=["Marcas"])
except Exception as e:
    print("⚠️  Módulo marca no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import locales as locales_module
    api_router.include_router(locales_module.router, prefix="/locales", tags=["Locales/Sucursales"])
except Exception as e:
    print("⚠️  Módulo locales no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import arqueos_caja as arqueos_caja_module
    api_router.include_router(arqueos_caja_module.router)
except Exception as e:
    print("⚠️  Módulo arqueos_caja no encontrado o error al importarlo:", e)

try:
    from app.api.v1.endpoints import retiros_caja as retiros_caja_module
    api_router.include_router(retiros_caja_module.router)
except Exception as e:
    print("⚠️  Módulo retiros_caja no encontrado o error al importarlo:", e)

# Añadir más includes similares según los módulos que tengas  
try:  
    from app.api.v1.endpoints import gastos as gastos_module  
    api_router.include_router(gastos_module.router, tags=["Gastos"])  
except Exception as e:  
    print("⚠️  Módulo gastos no encontrado o error al importarlo:", e) 

# Promociones
try:
    from app.api.v1.endpoints import promociones as promociones_module
    api_router.include_router(promociones_module.router, prefix="/promociones", tags=["Promociones"])
except Exception as e:
    print("⚠️  Módulo promociones no encontrado o error al importarlo:", e)

# Asistencia de empleados (RRHH)
try:
    from app.api.v1.endpoints import asistencia as asistencia_module
    api_router.include_router(asistencia_module.router, tags=["Asistencia RRHH"])
except Exception as e:
    print("⚠️  Módulo asistencia no encontrado o error al importarlo:", e)
