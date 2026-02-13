# SOLUCIÓN: HTTPS Proxy Configuration y horaEl Reference Error

## Problemas Identificados

1. **Error `horaEl is not defined`** en cierre_caja_nuevo.html (línea 336)
2. **Mixed Content Error** - Page HTTPS + Resources HTTP
   - `http://refaccionaria-oviedo-production.up.railway.app/api/v1/...`

## Soluciones Implementadas

### 1. Error `horaEl` - ✅ RESUELTO

**Archivo:** `app/static/cierre_caja_nuevo.html`

**Problema:** La función `init()` accedía a variable `horaEl` sin defini rla.

**Corrección:**
```javascript
function init() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const now = new Date();  // ✅ Definir fecha actual

    // ✅ Obtener elementos del DOM correctamente
    const fechaEl = $('fecha');
    if (fechaEl) {
        fechaEl.textContent = now.toLocaleDateString('es-MX');
    }

    const horaEl = $('hora');  // ✅ Definir antes de usar
    if (horaEl) {
        horaEl.textContent = now.toLocaleTimeString('es-MX');
    }
    // ... resto del código
}
```

---

### 2. Mixed Content en Railway - ✅ RESUELTO

#### ¿Por qué pasaba?

Railway usa arquitectura de proxy reverso:

```
[CLIENTE HTTPS] → [RAILWAY PROXY HTTPS] → [FastAPI APP HTTP] → [MYSQL]
      ↓                                              ↓
   Navegador cree que                        FastAPI solo recibe
   está en HTTPS                             peticiones HTTP
```

Sin configuración: FastAPI genera URLs HTTP → Navegador rechaza (Mixed Content)

#### Solución 1: Dockerfile Actualizado

**Archivo:** `Dockerfile`

```dockerfile
CMD ["uvicorn", "app.main:app", 
     "--host", "0.0.0.0", 
     "--port", "8000", 
     "--proxy-headers",           # ✅ Lee X-Forwarded-* headers
     "--forwarded-allow-ips", "*"] # ✅ Acepta desde cualquier IP
```

**¿Qué hacen estos flags?**
- `--proxy-headers`: Uvicorn lee headers del proxy (X-Forwarded-Proto, X-Forwarded-For, etc)
- `--forwarded-allow-ips "*"`: Acepta headers de proxy desde Railway (no verifica IP)

#### Solución 2: Middleware TrustedHostMiddleware

**Archivo:** `app/main.py`

```python
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Railway maneja hosts
)
```

#### Solución 3: Middleware HTTPS Security

**Archivo:** `app/main.py`

```python
class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if settings.ENVIRONMENT == "production":
            response = await call_next(request)
            # Fuerza HTTPS en futuros requests
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            return response
        return await call_next(request)
```

#### Solución 4: CORS Configuration

**Archivo:** `app/core/config.py`

```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",          # Desarrollo local
    "http://localhost:8000",          # Desarrollo local
    "https://refaccionaria-oviedo-production.up.railway.app",  # Producción
    "https://refaccionaria-oviedo.up.railway.app",             # Producción alt
]
```

#### Solución 5: Orden Correcto de Middlewares

**Archivo:** `app/main.py`

```python
# Orden crítico (se ejecutan en ORDEN REVERSO):
app.add_middleware(HTTPSRedirectMiddleware)      # Last added = First executed
app.add_middleware(TrustedHostMiddleware, ...)   # Middle
app.add_middleware(CORSMiddleware, ...)          # First added = Last executed (base)
```

---

## Configuración en Railway

### Variables de Entorno Obligatorias

En Railway Dashboard → Your Service → Settings → Variables:

```
ENVIRONMENT=production
DEBUG=false
```

### Variables de Base de Datos

```
DATABASE_URL=mysql+pymysql://usuario:pass@host:3306/refaccionaria_db
```

O alternativamente:
```
MYSQL_SERVER=<host_remoto>
MYSQL_USER=usuario
MYSQL_PASSWORD=contraseña
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
```

---

## Cómo Desplegar

1. **Commit cambios:**
```bash
git add .
git commit -m "Fix: HTTPS proxy headers and horaEl initialization"
git push origin Ricardo
```

2. **Railway reiniciará automáticamente**

3. **Verifica en navegador:**
```
https://refaccionaria-oviedo-production.up.railway.app
```

---

## Verificar que Funciona

Abre DevTools (F12) y verifica:

1. **Console:**
   - ❌ No debe haber `Mixed Content` error
   - ❌ No debe haber `horaEl is not defined`

2. **Network Tab:**
   - Solicitudes a `/api/v1/*` deben ser HTTPS ✅
   - Status 200/401 normal, no 400+ por Mixed Content

3. **Headers de Response:**
   - Busca header: `Strict-Transport-Security`
   - Valor: `max-age=31536000; includeSubDomains` ✅

4. **Application Tab:**
   - Verifica que localStorage tiene `access_token`
   - Verifica `sucursal_nombre` está guardado

---

## Resumen de Cambios

| Archivo | Cambio |
|---------|--------|
| `Dockerfile` | Agregar `--proxy-headers --forwarded-allow-ips "*"` |
| `app/main.py` | Agregar middlewares TrustedHost + HTTPS |
| `app/core/config.py` | CORS con URLs HTTPS de producción |
| `app/static/cierre_caja_nuevo.html` | Inicializar `horaEl` y fecha |
| `.env.example` | Documentar variables de producción |

---

## Si Persisten Errores

### Caso 1: Aún ve `http://` en Network
```
✅ Limpia caché: Ctrl+Shift+Delete → Sitios
✅ Prueba en incógnito
✅ Verifica ENVIRONMENT=production en Railway
```

### Caso 2: 502 Bad Gateway
```
✅ Revisa Logs en Railway
✅ Verifica DATABASE_URL está correcta
✅ Espera 2-3 minutos para que Railway reinicie
```

### Caso 3: Aún ve horaEl error
```
✅ Hard refresh: Ctrl+F5
✅ Borra cache: F12 → Application → Clear Site Data
```

---

## Flujo Técnico Ahora Correcto

```
[Cliente HTTPS] 
  ↓ Carga cierre_caja_nuevo.html
[Railway Proxy]
  ↓ X-Forwarded-Proto: https
  ↓ X-Forwarded-Host: refaccionaria-oviedo-production.up.railway.app
[FastAPI con --proxy-headers]
  ↓ Lee estos headers
  ↓ Entiende que está en HTTPS
  ↓ Genera respuestas HTTPS-aware
[Navegador]
  ↓ Recibe: https://... + https://api/v1/...
  ✅ Válido, sin Mixed Content
```

Sin los cambios:
```
[FastAPI sin --proxy-headers]
  ↓ Ignora headers de proxy
  ↓ Genera URL basada en HTTP directo
[Navegador]
  ↓ Recibe: https://... + http://api/v1/...
  ❌ MIXED CONTENT ERROR
```

---

## Prueba Rápida de Salud

```bash
# Desde terminal
curl -v https://refaccionaria-oviedo-production.up.railway.app/health

# Debería ver:
# - Status 200 OK
# - Headers con HTTPS (no 301 redirect)
# - Header: Strict-Transport-Security
# - Body: {"status":"healthy","service":"refaccionaria-api",...}
```
